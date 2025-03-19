import os
import uuid

import boto3
from botocore.exceptions import ClientError
from starlette.datastructures import UploadFile

from config import APP_SETTINGS
from .base import StorageManager


class S3StorageManager(StorageManager):
    file_classes = (UploadFile,)
    aws_access_key_id = APP_SETTINGS.AWS_ACCESS_KEY_ID
    aws_secret_access_key = APP_SETTINGS.AWS_SECRET_ACCESS_KEY
    region_name = None
    bucket_name = APP_SETTINGS.AWS_BUCKET_NAME
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
    )
    file_host = f"https://{bucket_name}.s3.amazonaws.com/"

    @classmethod
    def save(cls, file_path: str, upload_folder: str) -> str:
        filename = os.path.basename(file_path)
        s3_key = f"{upload_folder}/{filename}"

        try:
            cls.s3_client.upload_file(file_path, cls.bucket_name, s3_key)
            return s3_key
        except ClientError as e:
            raise ValueError(f"File upload failed: {e}")

    @classmethod
    def save_bytes(cls, file_bytes: bytes, upload_folder: str) -> str:
        filename = f"{uuid.uuid4()}.jpeg"
        s3_key = f"{upload_folder}/{filename}"

        try:
            cls.s3_client.put_object(
                Bucket=cls.bucket_name,
                Key=s3_key,
                Body=file_bytes,
                ContentType="image/jpeg"
            )
            return s3_key
        except ClientError as e:
            raise ValueError(f"File upload failed: {e}")

    @classmethod
    def delete(cls, path: str, upload_folder: str):
        s3_key = f"{upload_folder}/{path}"
        try:
            cls.s3_client.delete_object(Bucket=cls.bucket_name, Key=s3_key)
        except ClientError as e:
            raise ValueError(f"File deletion failed: {e}")
