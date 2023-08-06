# -*- coding: utf-8 -*-
"""Library to simplify working with S3."""
import os
from typing import Any, Optional, List

import boto3
from aws_lambda_powertools import Logger
from botocore.config import Config
from botocore.exceptions import ClientError

LOGGER = Logger(sampling_rate=float(os.environ["LOG_SAMPLING_RATE"]), level=os.environ["LOG_LEVEL"])


class S3Service:
    """Simplify S3 actions."""

    def __init__(self, region_name="eu-west-1"):
        """Initialize default AWS region name.

        :param region_name: default eu-west-1
        """
        self.__s3 = boto3.client(
            "s3", region_name=region_name, config=Config(retries={"max_attempts": 10, "mode": "adaptive"})
        )

    def upload(self, *, bucket: str, local_path: str, remote_path: str, extra_args=None) -> None:
        """Upload files from local path to target path on S3 bucket.

        :param bucket: S3 bucket name
        :param local_path: local file path
        :param remote_path: target file path
        :param extra_args: extra arguments for upload
        :return:
        """
        if extra_args is None:
            extra_args = {}
        try:
            self.__s3.upload_file(local_path, bucket, remote_path, ExtraArgs=extra_args)
            LOGGER.info(f"Uploaded file {local_path} into s3://{bucket}/{remote_path}")
        except ClientError:
            LOGGER.error(f"Failed to upload file {local_path} into s3://{bucket}/{remote_path}")
            raise

    def download(self, *, bucket: str, local_path: str, remote_path: str) -> None:
        """Download files from path in S3 bucket to local path.

        :param bucket: S3 bucket name
        :param local_path: local file path
        :param remote_path: target file path
        :return:
        """
        try:
            self.__s3.download_file(bucket, remote_path, local_path)
            LOGGER.info(f"Downloaded file s3://{bucket}/{remote_path} into {local_path}")
        except ClientError:
            LOGGER.error("Failed to download file s3://{bucket}/{remote_path} into {local_path}")
            raise

    def list_files(self, *, bucket: str, prefix: str, page_size=1000) -> List[Optional[Any]]:
        """List files using prefix path in S3 bucket.

        :param bucket: S3 bucket name
        :param prefix: prefix path
        :param page_size: number of files to return per page
        :return:
        """
        try:
            token = None
            files: list[str] = []
            while True:
                if token is None:
                    response = self.__s3.list_objects_v2(Bucket=bucket, Prefix=prefix, MaxKeys=page_size)
                else:
                    response = self.__s3.list_objects_v2(
                        Bucket=bucket,
                        Prefix=prefix,
                        MaxKeys=page_size,
                        ContinuationToken=token,
                    )
                if "Contents" in response.keys():
                    files.extend(file["Key"] for file in response["Contents"])
                if response["IsTruncated"]:
                    token = response["NextContinuationToken"]
                else:
                    break
            LOGGER.info(f"Found {len(files)} search results with prefix {prefix}")
            return files
        except ClientError:
            LOGGER.error(f"Failed to list files in bucket {bucket} with prefix {prefix}")
            raise

    def list_prefixes(self, *, bucket, delimiter, path_prefix="", page_size=1000) -> list[Any | None]:
        """List prefixes that are in path prefix in S3 bucket.

        :param bucket: S3 bucket name
        :param delimiter: delimiter
        :param path_prefix: prefix path
        :param page_size: number of files to return per page
        :return:
        """
        try:
            token = None
            prefixes: list[str] = []
            while True:
                if token is None:
                    response = self.__s3.list_objects_v2(
                        Bucket=bucket,
                        Prefix=path_prefix,
                        Delimiter=delimiter,
                        MaxKeys=page_size,
                    )
                else:
                    response = self.__s3.list_objects_v2(
                        Bucket=bucket,
                        Prefix=path_prefix,
                        Delimiter=delimiter,
                        MaxKeys=page_size,
                        ContinuationToken=token,
                    )
                if "CommonPrefixes" in response.keys():
                    prefixes.extend(
                        prefix["Prefix"].replace(path_prefix, "").replace(delimiter, "")
                        for prefix in response["CommonPrefixes"]
                    )

                if response["IsTruncated"]:
                    token = response["NextContinuationToken"]
                else:
                    break
            LOGGER.info(f"Found {len(prefixes)} prefixes with delimiter {delimiter}")
            return prefixes
        except ClientError:
            LOGGER.error(f"Failed to list prefixes in bucket {bucket} with delimiter {delimiter}")
            raise

    def delete_object(self, *, bucket: str, key: str) -> None:
        """Delete file from S3 bucket.

        :param bucket: S3 bucket name
        :param key: file key
        :return:
        """
        try:
            self.__s3.delete_object(Bucket=bucket, Key=key)
            LOGGER.info(f"Deleted file s3://{bucket}/{key}")
        except ClientError as client_error:
            if client_error.response["Error"]["Code"] == "404":
                LOGGER.exception(f"Object not found: {bucket}, {key}")
            LOGGER.error(f"Failed to delete file s3://{bucket}/{key}")
            raise

    def delete_objects(self, *, bucket: str, keys: List[Optional[Any]]):
        """Delete files from S3 bucket.

        :param bucket: S3 bucket name
        :param keys: list of S3 objects to be removed
        """
        try:
            for idx in range(0, len(keys), 1000):
                objects = [{"Key": key} for key in keys[idx : idx + 1000]]
                self.__s3.delete_objects(Bucket=bucket, Delete={"Objects": objects})
            LOGGER.info(f"Deleted {len(keys)} objects from bucket {bucket}")
        except ClientError:
            LOGGER.error(f"Failed to delete objects from bucket {bucket}")
            raise

    def delete_prefix(self, *, bucket: str, prefix: str):
        """Delete all files from S3 bucket that have the same prefix.

        :param bucket: S3 bucket name
        :param prefix: prefix path
        """
        LOGGER.info(f"Deleting prefix {prefix} from bucket {bucket}")
        keys = self.list_files(bucket=bucket, prefix=prefix)
        self.delete_objects(bucket=bucket, keys=keys)
        LOGGER.info(f"Deleted prefix {prefix} from bucket {bucket}")

    def copy(self, *, source_bucket: str, source_key: str, target_bucket: str, target_key: str):
        # sourcery skip: raise-specific-error
        """Copy file from S3 bucket to another S3 location."""
        try:
            copy_source = {"Bucket": source_bucket, "Key": source_key}
            self.__s3.copy(copy_source, target_bucket, target_key)
        except ClientError as error:
            if error.response["Error"]["Code"] == "404":
                LOGGER.error(
                    f"Failed to copy objects s3://{source_bucket}/{source_key} -> s3://{target_bucket}/{target_key}"
                )

        except Exception as error:
            LOGGER.critical(f"Unexpected error in download_object function of s3 helper: {error}")
            raise Exception(f"Unexpected error in download_object function of s3 helper: {error}") from error

    def move_object(self, *, source_bucket: str, source_key: str, target_bucket: str, target_key: str):
        """Move file from S3 bucket to another S3 location.

        :param source_bucket: S3 bucket name
        :param source_key: file key
        :param target_bucket: S3 bucket name
        :param target_key: file key
        :return:
        """
        try:
            self.copy(
                source_bucket=source_bucket, source_key=source_key, target_bucket=target_bucket, target_key=target_key
            )
            self.delete_object(bucket=source_bucket, key=source_key)
            LOGGER.info(f"Object moved s3://{source_bucket}/{source_key} -> s3://{target_bucket}/{target_key}")
        except ClientError:
            LOGGER.error(
                f"Failed to move object s3://{source_bucket}/{source_key} -> s3://{target_bucket}/{target_key}"
            )
            raise

    def move_objects(self, *, source_bucket: str, source_prefix: str, target_bucket: str, target_prefix: str):
        """Move files from S3 bucket to another S3 location.

        :param  source_bucket: S3 bucket name
        :param source_prefix: prefix path
        :param target_bucket: S3 bucket name
        :param target_prefix: prefix path
        :return:
        """
        try:
            LOGGER.info(
                f"Starting moving objects s3://{source_bucket}/{source_prefix} -> s3://{target_bucket}/{target_prefix}",
            )
            token = None
            while True:
                if token is None:
                    response = self.__s3.list_objects_v2(Bucket=source_bucket, Prefix=source_prefix, MaxKeys=1000)
                else:
                    response = self.__s3.list_objects_v2(
                        Bucket=source_bucket,
                        Prefix=source_prefix,
                        MaxKeys=1000,
                        ContinuationToken=token,
                    )
                if "Contents" in response.keys():
                    for file in response["Contents"]:
                        if file["Key"] == source_prefix:
                            continue
                        target_key = f"{file['Key'].replace(source_prefix, target_prefix)}"
                        self.move_object(
                            source_bucket=source_bucket,
                            source_key=file["Key"],
                            target_bucket=target_bucket,
                            target_key=target_key,
                        )
                if response["IsTruncated"]:
                    token = response["NextContinuationToken"]
                else:
                    break
            LOGGER.info(
                f"Finished moving objects s3://{source_bucket}/{source_prefix} -> s3://{target_bucket}/{target_prefix}",
            )
        except ClientError:
            LOGGER.error(
                "Failed to move objects s3://{source_bucket}/{source_prefix} -> s3://{target_bucket}/{target_prefix}"
            )
            raise
