[![auto-merge](https://github.com/airmonitor/aws-hexagonal-adapters/actions/workflows/auto_merge.yml/badge.svg)](https://github.com/airmonitor/aws-hexagonal-adapters/actions/workflows/auto_merge.yml)
[![tests](https://github.com/airmonitor/aws-hexagonal-adapters/actions/workflows/tests.yml/badge.svg)](https://github.com/airmonitor/aws-hexagonal-adapters/actions/workflows/tests.yml)

# aws-hexagonal-adapters
Adapters following hexagonal architecture to connect various AWS services


# Example usage

## S3
### Download object
```python
from os import environ

from aws_hexagonal_adapters.s3_service import S3Service

S3_SERVICE = S3Service(region_name=environ["CURRENT_REGION"])

# Download file
S3_SERVICE.download(
    bucket="bucket_name", local_path=f"/tmp/object", remote_path="object"
)
```

### Upload object
```python
from os import environ

from aws_hexagonal_adapters.s3_service import S3Service

S3_SERVICE = S3Service(region_name=environ["CURRENT_REGION"])

# Download file
S3_SERVICE.upload(
    bucket="bucket_name",
    local_path=f"/tmp/object_name",
    remote_path="object_name",
    extra_args={"StorageClass": "STANDARD_IA"},
)
```

### List objects
```python
from os import environ

from aws_hexagonal_adapters.s3_service import S3Service

S3_SERVICE = S3Service(region_name=environ["CURRENT_REGION"])

# Download file
S3_SERVICE.list_files(bucket="bucket_name", prefix="folder_name")
```


### Delete object
```python
from os import environ

from aws_hexagonal_adapters.s3_service import S3Service

S3_SERVICE = S3Service(region_name=environ["CURRENT_REGION"])

# Download file
S3_SERVICE.delete_object(bucket="bucket_name", key="object_name")
```


### Delete objects
```python
from os import environ

from aws_hexagonal_adapters.s3_service import S3Service

S3_SERVICE = S3Service(region_name=environ["CURRENT_REGION"])
objects = ["folder/object1.txt", "folder/object2.txt", "folder/object3.txt"]
# Download file
S3_SERVICE.delete_objects(bucket="bucket_name", keys=objects)
```
