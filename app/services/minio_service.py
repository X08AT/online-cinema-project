import uuid

from fastapi import UploadFile
from minio import Minio

from app.core.settings import settings

minio_client = Minio(
    endpoint=settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ROOT_USER,
    secret_key=settings.MINIO_ROOT_PASSWORD,
    secure=False
)


def ensure_bucket_exists(bucket_name: str):
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)


def upload_avatar(file: UploadFile) -> str:
    avatar_path = f"avatars/{uuid.uuid4()}-{file.filename}"
    ensure_bucket_exists(settings.MINIO_BUCKET)
    minio_client.put_object(
        bucket_name=settings.MINIO_BUCKET,
        object_name=avatar_path,
        data=file.file,
        length=-1,
        part_size=10 * 1024 * 1024,
        content_type=file.content_type
    )
    return avatar_path
