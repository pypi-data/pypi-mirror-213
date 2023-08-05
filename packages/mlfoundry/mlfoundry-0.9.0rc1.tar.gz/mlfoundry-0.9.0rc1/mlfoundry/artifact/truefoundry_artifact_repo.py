import math
import mmap
import os
import posixpath
import typing
import uuid
from concurrent.futures import FIRST_EXCEPTION, ThreadPoolExecutor, wait
from threading import Event
from typing import List, NamedTuple, Optional, Tuple

import requests
from mlflow.entities import (
    ArtifactType,
    FileInfo,
    MultiPartUpload,
    MultiPartUploadStorageProvider,
    SignedURL,
)
from mlflow.store.artifact.artifact_repo import ArtifactRepository
from mlflow.tracking import MlflowClient
from mlflow.utils.file_utils import (
    download_file_using_http_uri,
    relative_path_to_artifact_path,
)
from mlflow.utils.rest_utils import cloud_storage_http_request
from tqdm.utils import CallbackIOWrapper

from mlfoundry.env_vars import DISABLE_MULTIPART_UPLOAD
from mlfoundry.exceptions import MlFoundryException
from mlfoundry.logger import logger
from mlfoundry.tracking.entities import ArtifactCredential
from mlfoundry.tracking.truefoundry_rest_store import TruefoundryRestStore

_MIN_BYTES_REQUIRED_FOR_MULTIPART = 100 * 1024 * 1024
_MULTIPART_DISABLED = os.getenv(DISABLE_MULTIPART_UPLOAD, "").lower() == "true"

# GCP/S3 Maximum number of parts per upload	10,000
# Maximum number of blocks in a block blob 50,000 blocks
# TODO: This number is artificially limited now. Later
# we will ask for parts signed URI in batches rather than in a single
# API Calls:
# Create Multipart Upload (Returns maximum number of parts, size limit of
#                            a single part, upload id for s3 etc )
#   Get me signed uris for first 500 parts
#     Upload 500 parts
#   Get me signed uris for the next 500 parts
#     Upload 500 parts
#   ...
# Finalize the Multipart upload using the finalize signed url returned
# by Create Multipart Upload or get a new one.
_MAX_NUM_PARTS_FOR_MULTIPART = 1000

# Azure Maximum size of a block in a block blob	4000 MiB
# GCP/S3 Maximum size of an individual part in a multipart upload 5 GiB
_MAX_PART_SIZE_BYTES_FOR_MULTIPART = 4 * 1024 * 1024 * 1000
_MAX_WORKERS_FOR_UPLOAD = max(min(32, os.cpu_count() * 2), 4)


def _allign_part_size_with_mmap_allocation_granularity(part_size: int) -> int:
    modulo = part_size % mmap.ALLOCATIONGRANULARITY
    if modulo == 0:
        return part_size

    part_size += mmap.ALLOCATIONGRANULARITY - modulo
    return part_size


# Can not be less than 5 * 1024 * 1024
_PART_SIZE_BYTES_FOR_MULTIPART = _allign_part_size_with_mmap_allocation_granularity(
    10 * 1024 * 1024
)


class TruefoundryArtifactRepository(ArtifactRepository):
    def __init__(
        self,
        artifact_uri,
        rest_store: TruefoundryRestStore,
        credentials=None,
        storage_integration_id=None,
    ):
        self.artifact_uri = artifact_uri
        super().__init__(artifact_uri)

        self.rest_store: TruefoundryRestStore = rest_store

    @staticmethod
    def _extract_run_id(artifact_uri) -> str:
        # artifact_uri will be something like,
        # s3://<BUCKET>/<PATH>/<EXP_ID>/<RUN_ID>/artifacts
        run_id = artifact_uri.rstrip("/").split("/")[-2]
        return run_id

    def list_artifacts(self, path=None) -> typing.List[FileInfo]:
        run_id = self._extract_run_id(self.artifact_uri)
        artifacts = self.rest_store.list_artifacts(run_id=run_id, path=path)
        return artifacts

    def _signed_uri_upload_file(
        self, artifact_credential: ArtifactCredential, local_file: str
    ):
        if os.stat(local_file).st_size == 0:
            with cloud_storage_http_request(
                "put",
                artifact_credential.signed_uri,
                data="",
            ) as response:
                response.raise_for_status()
        else:
            with open(local_file, "rb") as file:
                with cloud_storage_http_request(
                    "put",
                    artifact_credential.signed_uri,
                    data=file,
                ) as response:
                    response.raise_for_status()

    def log_artifacts(self, local_dir, artifact_path=None):
        dest_path = artifact_path or ""
        dest_path = dest_path.lstrip(posixpath.sep)
        for (root, _, file_names) in os.walk(local_dir):
            upload_path = dest_path
            if root != local_dir:
                rel_path = os.path.relpath(root, local_dir)
                rel_path = relative_path_to_artifact_path(rel_path)
                upload_path = posixpath.join(dest_path, rel_path)
            for file_name in file_names:
                local_file = os.path.join(root, file_name)
                self.log_artifact(local_file=local_file, artifact_path=upload_path)

    def log_artifact(self, local_file, artifact_path=None):
        dest_path = artifact_path or ""
        dest_path = dest_path.lstrip(posixpath.sep)
        dest_path = posixpath.join(dest_path, os.path.basename(local_file))
        artifact_credential = self.rest_store.get_artifact_write_credential(
            run_id=self._extract_run_id(self.artifact_uri), path=dest_path
        )
        self._signed_uri_upload_file(artifact_credential, local_file)

    def _download_file(self, remote_file_path: str, local_path: str):
        if not remote_file_path:
            raise MlFoundryException(
                f"remote_file_path cannot be None or empty str {remote_file_path}"
            )

        artifact_credential = self.rest_store.get_artifact_read_credentials(
            run_id=self._extract_run_id(self.artifact_uri), path=remote_file_path
        )
        download_file_using_http_uri(
            http_uri=artifact_credential.signed_uri, download_path=local_path
        )


class _PartNumberEtag(NamedTuple):
    part_number: int
    etag: str


def _get_s3_compatible_completion_body(multi_parts: List[_PartNumberEtag]) -> str:
    body = "<CompleteMultipartUpload>\n"
    for part in multi_parts:
        body += "  <Part>\n"
        body += f"    <PartNumber>{part.part_number}</PartNumber>\n"
        body += f"    <ETag>{part.etag}</ETag>\n"
        body += "  </Part>\n"
    body += "</CompleteMultipartUpload>"
    return body


def _get_azure_blob_completion_body(block_ids: List[str]) -> str:
    body = "<BlockList>\n"
    for block_id in block_ids:
        body += f"<Uncommitted>{block_id}</Uncommitted> "
    body += "</BlockList>"
    return body


class _FileMultiPartInfo(NamedTuple):
    num_parts: int
    part_size: int
    file_size: int


def _decide_file_parts(file_path: str) -> _FileMultiPartInfo:
    file_size = os.path.getsize(file_path)
    if file_size < _MIN_BYTES_REQUIRED_FOR_MULTIPART or _MULTIPART_DISABLED:
        return _FileMultiPartInfo(1, part_size=file_size, file_size=file_size)

    ideal_num_parts = math.ceil(file_size / _PART_SIZE_BYTES_FOR_MULTIPART)
    if ideal_num_parts <= _MAX_NUM_PARTS_FOR_MULTIPART:
        return _FileMultiPartInfo(
            ideal_num_parts,
            part_size=_PART_SIZE_BYTES_FOR_MULTIPART,
            file_size=file_size,
        )

    part_size_when_using_max_parts = math.ceil(file_size / _MAX_NUM_PARTS_FOR_MULTIPART)
    part_size_when_using_max_parts = _allign_part_size_with_mmap_allocation_granularity(
        part_size_when_using_max_parts
    )
    if part_size_when_using_max_parts > _MAX_PART_SIZE_BYTES_FOR_MULTIPART:
        raise ValueError(
            f"file {file_path!r} is too big for upload. Multipart chunk"
            f" size {part_size_when_using_max_parts} is higher"
            f" than {_MAX_PART_SIZE_BYTES_FOR_MULTIPART}"
        )
    num_parts = math.ceil(file_size / part_size_when_using_max_parts)
    return _FileMultiPartInfo(
        num_parts, part_size=part_size_when_using_max_parts, file_size=file_size
    )


def _signed_uri_upload_file(
    signed_url: SignedURL, local_file: str, abort_event: Optional[Event] = None
):
    if os.stat(local_file).st_size == 0:
        with cloud_storage_http_request("put", signed_url.url, data="") as response:
            response.raise_for_status()
            return

    def callback(*_, **__):
        if abort_event and abort_event.is_set():
            raise Exception("aborting upload")

    with open(local_file, "rb") as file:
        # NOTE: Azure Put Blob does not support Transfer Encoding header.
        wrapped_file = CallbackIOWrapper(callback, file, "read")
        with cloud_storage_http_request(
            "put", signed_url.url, data=wrapped_file
        ) as response:
            response.raise_for_status()


class _CallbackIOWrapperForMultiPartUpload(CallbackIOWrapper):
    def __init__(self, callback, stream, method, length: int):
        self.wrapper_setattr("_length", length)
        super().__init__(callback, stream, method)

    def __len__(self):
        return self.wrapper_getattr("_length")


def _file_part_upload(
    url: str,
    file_path: str,
    seek: int,
    length: int,
    file_size: int,
    abort_event: Optional[Event] = None,
    method: str = "put",
):
    def callback(*_, **__):
        if abort_event and abort_event.is_set():
            raise Exception("aborting upload")

    with open(file_path, "rb") as file:
        with mmap.mmap(
            file.fileno(),
            length=min(file_size - seek, length),
            offset=seek,
            access=mmap.ACCESS_READ,
        ) as mapped_file:
            wrapped_file = _CallbackIOWrapperForMultiPartUpload(
                callback, mapped_file, "read", len(mapped_file)
            )
            with cloud_storage_http_request(
                method,
                url,
                data=wrapped_file,
            ) as response:
                response.raise_for_status()
                return response


def _s3_compatible_multipart_upload(
    multipart_upload: MultiPartUpload,
    local_file: str,
    multipart_info: _FileMultiPartInfo,
    executor: ThreadPoolExecutor,
    abort_event: Optional[Event] = None,
):
    abort_event = abort_event or Event()
    parts = []

    def upload(part_number: int, seek: int):
        logger.debug(
            "Uploading part %d/%d of %s",
            part_number,
            multipart_info.num_parts,
            local_file,
        )
        response = _file_part_upload(
            url=multipart_upload.part_signed_urls[part_number].url,
            file_path=local_file,
            seek=seek,
            length=multipart_info.part_size,
            file_size=multipart_info.file_size,
            abort_event=abort_event,
        )
        logger.debug(
            "Uploaded part %d/%d of %s",
            part_number,
            multipart_info.num_parts,
            local_file,
        )
        etag = response.headers["ETag"]
        parts.append(_PartNumberEtag(etag=etag, part_number=part_number + 1))

    futures = []
    for part_number, seek in enumerate(
        range(0, multipart_info.file_size, multipart_info.part_size)
    ):
        future = executor.submit(upload, part_number=part_number, seek=seek)
        futures.append(future)

    done, not_done = wait(futures, return_when=FIRST_EXCEPTION)
    if len(not_done) > 0:
        abort_event.set()
    for future in not_done:
        future.cancel()
    for future in done:
        if future.exception() is not None:
            raise future.exception()

    logger.debug("Finalizing multipart upload of %s", local_file)
    parts = sorted(parts, key=lambda part: part.part_number)
    response = requests.post(
        multipart_upload.finalize_signed_url.url,
        data=_get_s3_compatible_completion_body(parts),
        timeout=2 * 60,
    )
    response.raise_for_status()
    logger.debug("Multipart upload of %s completed", local_file)


def _azure_multi_part_upload(
    multipart_upload: MultiPartUpload,
    local_file: str,
    multipart_info: _FileMultiPartInfo,
    executor: ThreadPoolExecutor,
    abort_event: Optional[Event] = None,
):
    abort_event = abort_event or Event()

    def upload(part_number: int, seek: int):
        logger.debug(
            "Uploading part %d/%d of %s",
            part_number,
            multipart_info.num_parts,
            local_file,
        )
        _file_part_upload(
            url=multipart_upload.part_signed_urls[part_number].url,
            file_path=local_file,
            seek=seek,
            length=multipart_info.part_size,
            file_size=multipart_info.file_size,
            abort_event=abort_event,
        )
        logger.debug(
            "Uploaded part %d/%d of %s",
            part_number,
            multipart_info.num_parts,
            local_file,
        )

    futures = []
    for part_number, seek in enumerate(
        range(0, multipart_info.file_size, multipart_info.part_size)
    ):
        future = executor.submit(upload, part_number=part_number, seek=seek)
        futures.append(future)

    done, not_done = wait(futures, return_when=FIRST_EXCEPTION)
    if len(not_done) > 0:
        abort_event.set()
    for future in not_done:
        future.cancel()
    for future in done:
        if future.exception() is not None:
            raise future.exception()

    logger.debug("Finalizing multipart upload of %s", local_file)
    response = requests.put(
        multipart_upload.finalize_signed_url.url,
        data=_get_azure_blob_completion_body(
            block_ids=multipart_upload.azure_blob_block_ids
        ),
        timeout=2 * 60,
    )
    response.raise_for_status()
    logger.debug("Multipart upload of %s completed", local_file)


class MlFoundryArtifactsRepository(ArtifactRepository):
    def __init__(self, version_id: uuid.UUID, mlflow_client: MlflowClient):
        self.version_id = version_id
        self._tracking_client = mlflow_client
        super().__init__(artifact_uri=None)

    # these methods should be named list_files, log_directory, log_file, etc

    def list_artifacts(self, path=None) -> typing.List[FileInfo]:
        return self._tracking_client.list_files_for_artifact_version(
            version_id=self.version_id, path=path
        )

    def log_artifacts(self, local_dir, artifact_path=None):
        dest_path = artifact_path or ""
        dest_path = dest_path.lstrip(posixpath.sep)

        files_for_normal_upload: List[Tuple[str, str, _FileMultiPartInfo]] = []
        files_for_multipart_upload: List[Tuple[str, str, _FileMultiPartInfo]] = []

        for (root, _, file_names) in os.walk(local_dir):
            upload_path = dest_path
            if root != local_dir:
                rel_path = os.path.relpath(root, local_dir)
                rel_path = relative_path_to_artifact_path(rel_path)
                upload_path = posixpath.join(dest_path, rel_path)
            for file_name in file_names:
                local_file = os.path.join(root, file_name)
                multipart_info = _decide_file_parts(local_file)
                if multipart_info.num_parts == 1:
                    files_for_normal_upload.append(
                        (upload_path, local_file, multipart_info)
                    )
                else:
                    files_for_multipart_upload.append(
                        (upload_path, local_file, multipart_info)
                    )

        abort_event = Event()
        with ThreadPoolExecutor(max_workers=_MAX_WORKERS_FOR_UPLOAD) as executor:
            futures = []
            for upload_path, local_file, multipart_info in files_for_normal_upload:
                future = executor.submit(
                    self._log_artifact,
                    local_file=local_file,
                    artifact_path=upload_path,
                    abort_event=abort_event,
                    multipart_info=multipart_info,
                )
                futures.append(future)

            done, not_done = wait(futures, return_when=FIRST_EXCEPTION)
            if len(not_done) > 0:
                abort_event.set()
            for future in not_done:
                future.cancel()
            for future in done:
                if future.exception() is not None:
                    raise future.exception()

            for upload_path, local_file, multipart_info in files_for_multipart_upload:
                self._log_artifact(
                    local_file=local_file,
                    artifact_path=upload_path,
                    multipart_info=multipart_info,
                    executor_for_multipart_upload=executor,
                )

    def _normal_upload(
        self, local_file: str, artifact_path: str, abort_event: Event = None
    ):
        signed_url = self._tracking_client.get_signed_urls_for_artifact_version_write(
            version_id=self.version_id, paths=[artifact_path]
        )[0]
        logger.info("Uploading %s to %s", local_file, artifact_path)
        _signed_uri_upload_file(
            signed_url=signed_url, local_file=local_file, abort_event=abort_event
        )
        logger.debug("Uploaded %s to %s", local_file, artifact_path)

    def _multipart_upload(
        self,
        local_file: str,
        artifact_path: str,
        multipart_info: _FileMultiPartInfo,
        executor: ThreadPoolExecutor,
        abort_event: Optional[Event] = None,
    ):
        logger.info(
            "Uploading %s to %s using multipart upload", local_file, artifact_path
        )
        multipart_upload = self._tracking_client.create_multipart_upload(
            artifact_version_id=self.version_id,
            path=artifact_path,
            num_parts=multipart_info.num_parts,
        )
        if (
            multipart_upload.storage_provider
            is MultiPartUploadStorageProvider.S3_COMPATIBLE
        ):
            _s3_compatible_multipart_upload(
                multipart_upload=multipart_upload,
                local_file=local_file,
                executor=executor,
                multipart_info=multipart_info,
                abort_event=abort_event,
            )
        elif (
            multipart_upload.storage_provider
            is MultiPartUploadStorageProvider.AZURE_BLOB
        ):
            _azure_multi_part_upload(
                multipart_upload=multipart_upload,
                local_file=local_file,
                executor=executor,
                multipart_info=multipart_info,
                abort_event=abort_event,
            )
        else:
            raise NotImplementedError()

    def _log_artifact(
        self,
        local_file: str,
        artifact_path: Optional[str],
        multipart_info: _FileMultiPartInfo,
        abort_event: Optional[Event] = None,
        executor_for_multipart_upload: Optional[ThreadPoolExecutor] = None,
    ):
        dest_path = artifact_path or ""
        dest_path = dest_path.lstrip(posixpath.sep)
        dest_path = posixpath.join(dest_path, os.path.basename(local_file))

        if multipart_info.num_parts == 1:
            return self._normal_upload(
                local_file=local_file, artifact_path=dest_path, abort_event=abort_event
            )

        if not executor_for_multipart_upload:
            with ThreadPoolExecutor(max_workers=_MAX_WORKERS_FOR_UPLOAD) as executor:
                return self._multipart_upload(
                    local_file=local_file,
                    artifact_path=dest_path,
                    executor=executor,
                    multipart_info=multipart_info,
                )

        return self._multipart_upload(
            local_file=local_file,
            artifact_path=dest_path,
            executor=executor_for_multipart_upload,
            multipart_info=multipart_info,
        )

    def log_artifact(self, local_file: str, artifact_path: Optional[str] = None):
        self._log_artifact(
            local_file=local_file,
            artifact_path=artifact_path,
            multipart_info=_decide_file_parts(local_file),
        )

    def _download_file(self, remote_file_path: str, local_path: str):
        if not remote_file_path:
            raise MlFoundryException(
                f"remote_file_path cannot be None or empty str {remote_file_path}"
            )
        # TODO (chiragjn): Re-implement download from parent to take advantage of getting multiple signed urls at once
        #                  However care also needs to be taken to expose and pass in proper expiry because the user
        #                  user might be on slow connections or downloading many files sequentially might eat up time
        signed_url = self._tracking_client.get_signed_urls_for_artifact_version_read(
            version_id=self.version_id, paths=[remote_file_path]
        )[0]
        download_file_using_http_uri(http_uri=signed_url.url, download_path=local_path)
