# -*- coding: utf-8 -*-
import os

import boto3
import pytest
from moto import mock_s3
from botocore.exceptions import ClientError

from aws_hexagonal_adapters.s3_service import S3Service

constants = {
    "bucket_name": "test-bucket",
    "local_path": "test.txt",
    "download_local_path": "test_download.txt",
    "remote_path": "folder/test.txt",
    "extra_args": {"StorageClass": "STANDARD_IA"},
    "content": "test content\n",
}


@pytest.fixture(scope="module")
def s3_client():
    """Mock S3 client using moto."""
    with mock_s3():
        yield boto3.client("s3", region_name="us-east-1")


@pytest.fixture(scope="module")
def s3_bucket(s3_client):
    """Create a mock S3 bucket."""
    bucket_name = constants.get("bucket_name")
    s3_client.create_bucket(Bucket=bucket_name)
    yield bucket_name


@pytest.fixture(scope="module")
def s3_service(s3_client):
    """Create a mock S3 bucket."""
    yield S3Service(region_name="us-east-1")


def test_upload(s3_client, s3_bucket, s3_service):
    """Test uploading a file to S3."""
    local_path = constants.get("local_path")
    remote_path = constants.get("remote_path")
    extra_args = constants.get("extra_args")
    s3_service.upload(bucket=s3_bucket, local_path=local_path, remote_path=remote_path, extra_args=extra_args)

    response = s3_client.get_object(Bucket=s3_bucket, Key=remote_path)
    assert response["Body"].read().decode() == constants.get("content")


def test_download(s3_client, s3_bucket, s3_service):
    """Test downloading a file from S3."""
    local_path = constants.get("local_path")
    download_local_path = constants.get("download_local_path")
    remote_path = constants.get("remote_path")
    extra_args = constants.get("extra_args")
    s3_service.upload(bucket=s3_bucket, local_path=local_path, remote_path=remote_path, extra_args=extra_args)

    s3_service.download(bucket=s3_bucket, remote_path=remote_path, local_path=download_local_path)

    with open(local_path) as f:
        assert f.read() == constants.get("content")
    os.remove(download_local_path)


def test_list_files(s3_client, s3_bucket, s3_service):
    """Test listing files in a bucket."""
    local_path = constants.get("local_path")
    remote_path = constants.get("remote_path")
    extra_args = constants.get("extra_args")
    s3_service.upload(bucket=s3_bucket, local_path=local_path, remote_path=remote_path, extra_args=extra_args)

    files = s3_service.list_files(bucket=s3_bucket, prefix="folder")
    assert files == [remote_path]


def test_delete_object(s3_client, s3_bucket, s3_service):
    """Test deleting a file to S3."""
    local_path = constants.get("local_path")
    remote_path = constants.get("remote_path")
    extra_args = constants.get("extra_args")
    s3_service.upload(bucket=s3_bucket, local_path=local_path, remote_path=remote_path, extra_args=extra_args)

    response = s3_client.get_object(Bucket=s3_bucket, Key=remote_path)
    assert response["Body"].read().decode() == constants.get("content")

    s3_service.delete_object(bucket=s3_bucket, key=remote_path)

    with pytest.raises(ClientError):
        s3_service.download(bucket=s3_bucket, local_path=local_path, remote_path=remote_path)


def test_delete_objects(s3_client, s3_bucket, s3_service):
    """Test deleting objects from S3."""
    # Upload objects to S3 for testing
    objects = ["folder/object1.txt", "folder/object2.txt", "folder/object3.txt"]
    for obj in objects:
        s3_client.put_object(Bucket=s3_bucket, Key=obj, Body=b"test content")

    s3_service.delete_objects(bucket=s3_bucket, keys=objects)

    # Check if objects were deleted
    list_objects = s3_service.list_files(bucket=s3_bucket, prefix="folder")
    assert len(list_objects) == 0
