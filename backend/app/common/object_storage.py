"""S3 storage with stable application URLs, including for private buckets."""

from functools import lru_cache
from pathlib import PurePosixPath

from app.core.config import settings


@lru_cache
def get_s3_client():
    import boto3
    from botocore.config import Config

    return boto3.client(
        "s3",
        endpoint_url=settings.S3_ENDPOINT,
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        region_name=settings.S3_REGION,
        config=Config(
            signature_version="s3v4",
            connect_timeout=10,
            read_timeout=30,
            retries={"max_attempts": 3},
            s3={"addressing_style": settings.S3_ADDRESSING_STYLE},
        ),
    )


def object_key(relative_path: str) -> str:
    path = PurePosixPath(relative_path)
    if (
        not relative_path
        or path.is_absolute()
        or ".." in path.parts
        or "\\" in relative_path
    ):
        raise ValueError("Invalid storage path")
    return f"{settings.S3_KEY_PREFIX.strip('/')}/{path.as_posix()}"


def put_image(relative_path: str, content: bytes, content_type: str) -> None:
    get_s3_client().put_object(
        Bucket=settings.S3_BUCKET,
        Key=object_key(relative_path),
        Body=content,
        ContentType=content_type,
    )


def delete_image(relative_path: str) -> None:
    get_s3_client().delete_object(
        Bucket=settings.S3_BUCKET, Key=object_key(relative_path)
    )


def image_url(relative_path: str) -> str:
    return get_s3_client().generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.S3_BUCKET, "Key": object_key(relative_path)},
        ExpiresIn=settings.S3_PRESIGNED_URL_EXPIRES,
    )
