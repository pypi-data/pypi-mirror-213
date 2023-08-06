"""S3 Collector for downloading files and folders."""
import os
import posixpath
from typing import List, Optional, Union

from boto3 import client
from botocore.exceptions import ClientError
from ML_management.collectors.collector_pattern import CollectorPattern


class S3FolderNotFound(Exception):
    """Define Version Not Found Exception."""

    def __init__(self, path: str, bucket: str):
        self.path = path
        self.bucket = bucket
        self.message = f'Folder "{path}" is not found in "{bucket}" bucket'
        super().__init__(self.message)

    def __reduce__(self):
        """Define reduce method to make exception picklable."""
        return (S3FolderNotFound, (self.path, self.bucket))


class S3BucketNotFound(Exception):
    """Define Bucket Not Found Exception."""

    def __init__(self, bucket: str):
        self.bucket = bucket
        self.message = f'Bucket "{bucket}" does not exist'
        super().__init__(self.message)

    def __reduce__(self):
        """Define reduce method to make exception picklable."""
        return (S3FolderNotFound, (self.bucket))


class S3ObjectNotFound(Exception):
    """Define Version Not Found Exception."""

    def __init__(self, path: str, bucket: str):
        self.path = path
        self.bucket = bucket
        self.message = f'Object "{path}" is not found in "{bucket}" bucket'
        super().__init__(self.message)

    def __reduce__(self):
        """Define reduce method to make exception picklable."""
        return (S3ObjectNotFound, (self.path, self.bucket))


class S3Collector(CollectorPattern):
    """Collector for S3 paths using boto3 library."""

    def __init__(self) -> None:
        self.default_url = os.environ.get("MLFLOW_S3_ENDPOINT_URL", "http://localhost:9000")
        self.default_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID", "minioadmin")
        self.default_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY", "minioadmin")

    @staticmethod
    def get_json_schema():
        """Return json schema."""
        return {
            "type": "object",
            "properties": {
                "local_path": {"type": "string"},
                "bucket": {"type": "string"},
                "remote_paths": {"type": "array", "items": {"type": "string"}},
                "service_name": {"type": "string"},
                "region_name": {"type": "string"},
                "api_version": {"type": "string"},
                "use_ssl": {"type": "boolean"},
                "verify": {
                    "anyOf": [
                        {"type": "boolean"},
                        {"type": "string"},
                    ]
                },
                "endpoint_url": {"type": "string"},
                "aws_access_key_id": {"type": "string"},
                "aws_secret_access_key": {"type": "string"},
                "aws_session_token": {"type": "string"},
            },
            "required": ["bucket"],
            "additionalProperties": False,
        }

    def _download_file(self, bucket: str, service_client, remote_file_path: str, local_path: str):
        dirpath = posixpath.dirname(remote_file_path)
        local_dir_path = os.path.join(local_path, dirpath)
        local_file_path = os.path.join(local_path, remote_file_path)
        if not os.path.exists(local_dir_path):
            os.makedirs(local_dir_path, exist_ok=True)
        try:
            with open(local_file_path, "wb") as _file:
                service_client.download_fileobj(bucket, remote_file_path, _file)
        except ClientError as err:
            if err.response["Error"]["Code"] == "404":
                # maybe user forgot to add trailing slash? Try to download as folder
                try:
                    remote_folder_path = remote_file_path + "/"
                    self._download_folder(bucket, service_client, remote_folder_path, local_path)
                except S3FolderNotFound:
                    try:
                        # maybe, bad bucket?
                        service_client.head_bucket(Bucket=bucket)
                    except ClientError as err:
                        if err.response["Error"]["Code"] == "404":
                            # bad bucket it is.
                            raise S3BucketNotFound(bucket=bucket)
                        else:
                            raise err
                    # bucket is ok, it is a bad object
                    raise S3ObjectNotFound(path=remote_file_path, bucket=bucket)  # attempt of search as a folder failed
            else:
                raise err
        return local_file_path

    def _download_folder(self, bucket, service_client, folder_path, local_path):
        paginator = service_client.get_paginator("list_objects_v2")
        # TODO prevent infinite loop, sometimes the dir is recursively included ???
        try:
            page_iterator = paginator.paginate(Bucket=bucket, Prefix=folder_path)
            for page in page_iterator:
                if page["KeyCount"] == 0:
                    # folder not found or is empty?
                    raise S3FolderNotFound(path=folder_path, bucket=bucket)
                # Objects listed directly will be files
                for obj in page.get("Contents", []):
                    file_path = obj.get("Key")
                    self._download_file(bucket, service_client, file_path, local_path)
        except ClientError as err:
            if err.response["Error"]["Code"] == "NoSuchBucket":
                raise S3BucketNotFound(bucket=bucket)
            else:
                raise err

    def set_data(
        self,
        *,
        local_path: str = "/s3_data/",
        bucket: str,  # TODO do we pass bucket or not? is it always possible to parse?
        remote_paths: Optional[List[str]] = None,
        service_name: str = "s3",
        region_name: Optional[str] = None,
        api_version: Optional[str] = None,
        use_ssl: bool = True,
        verify: Optional[Union[bool, str]] = None,
        endpoint_url: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None,
    ) -> str:
        """
        Set data.

        :type local_path: string
        :param local_path: Local path to save data to.  Defaults to /s3_data/.

        :type bucket: string
        :param bucket: Bucket containing requested files.

        :type remote_paths: list(string)
        :param remote_paths: List of paths relative to passed bucket.  Each path
            can represent either a single file, or a folder.  If a path represents
            a folder (should end with a slash), then all contents of a folder are recursively downloaded.

        :type service_name: string
        :param service_name: The name of a service, e.g. 's3' or 'ec2'
        available to boto3.  Defaults to 's3'.

        :type region_name: string
        :param region_name: The name of the region associated with the client.
            A client is associated with a single region.

        :type api_version: string
        :param api_version: The API version to use.  By default, botocore will
            use the latest API version when creating a client.  You only need
            to specify this parameter if you want to use a previous API version
            of the client.

        :type use_ssl: boolean
        :param use_ssl: Whether to use SSL.  By default, SSL is used.
            Note that not all services support non-ssl connections.

        :type verify: boolean/string
        :param verify: Whether to verify SSL certificates.  By default,
            SSL certificates are verified.  You can provide the following
            values:

            * False - do not validate SSL certificates.  SSL will still be
              used (unless use_ssl is False), but SSL certificates
              will not be verified.
            * path/to/cert/bundle.pem - A filename of the CA cert bundle to
              uses.  You can specify this argument if you want to use a
              different CA cert bundle than the one used by botocore.

        :type endpoint_url: string
        :param endpoint_url: The complete URL to use for the constructed
            client. Normally, botocore will automatically construct the
            appropriate URL to use when communicating with a service.  You
            can specify a complete URL (including the "http/https" scheme)
            to override this behavior.  If this value is provided,
            then ``use_ssl`` is ignored.

        :type aws_access_key_id: string
        :param aws_access_key_id: The access key to use when creating
            the client.  This is entirely optional, and if not provided,
            the credentials configured for the session will automatically
            be used.  You only need to provide this argument if you want
            to override the credentials used for this specific client.

        :type aws_secret_access_key: string
        :param aws_secret_access_key: The secret key to use when creating
            the client.  Same semantics as aws_access_key_id above.

        :type aws_session_token: string
        :param aws_session_token: The session token to use when creating
            the client.  Same semantics as aws_access_key_id above.
        """
        service_client = client(
            service_name=service_name,
            region_name=region_name,
            api_version=api_version,
            use_ssl=use_ssl,
            verify=verify,
            endpoint_url=endpoint_url if endpoint_url else self.default_url,
            aws_access_key_id=aws_access_key_id if aws_access_key_id else self.default_access_key_id,
            aws_secret_access_key=aws_secret_access_key if aws_secret_access_key else self.default_secret_access_key,
            aws_session_token=aws_session_token,
        )
        if remote_paths is not None:
            for path in remote_paths:
                if path.endswith("/"):
                    # it is a folder
                    # list all files in a folder in one go and download them all!
                    self._download_folder(bucket, service_client, path, local_path)
                else:
                    # it is a file
                    self._download_file(bucket, service_client, path, local_path)
        else:
            for key in service_client.list_objects(Bucket=bucket)["Contents"]:
                self._download_file(bucket, service_client, key["Key"], local_path)
        return local_path
