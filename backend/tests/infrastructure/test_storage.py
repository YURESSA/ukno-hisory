from io import BytesIO

import boto3
import pytest
from botocore.config import Config
from botocore.stub import ANY, Stubber
from fastapi import UploadFile
from sqlalchemy.engine import make_url
from starlette.datastructures import Headers

from app.common import object_storage
from app.common.file_storage import ImageStorage
from app.core.config import Settings, settings


def test_postgres_password_reserved_characters():
    config = Settings(
        _env_file=None, DB_BACKEND="postgres", POSTGRES_PASSWORD="p@ss:%/#?+"
    )
    assert make_url(config.DATABASE_URL).password == "p@ss:%/#?+"


def test_local_defaults_need_no_external_credentials():
    config = Settings(_env_file=None)
    assert config.DB_BACKEND == "sqlite"
    assert config.STORAGE_BACKEND == "local"


@pytest.mark.asyncio
async def test_private_s3_upload_and_delete_keep_stable_url(monkeypatch, uploads_dir):
    tmp_path = uploads_dir
    monkeypatch.setattr(settings, "STORAGE_BACKEND", "s3")
    monkeypatch.setattr(settings, "S3_BUCKET", "test-bucket")
    monkeypatch.setattr(settings, "S3_KEY_PREFIX", "5history")
    client = boto3.client(
        "s3",
        endpoint_url="https://s3.example.com",
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="ru-1",
        config=Config(signature_version="s3v4"),
    )
    monkeypatch.setattr(object_storage, "get_s3_client", lambda: client)
    storage = ImageStorage(tmp_path / "images", "/uploads/timeline")
    image = UploadFile(
        BytesIO(b"image-data"),
        filename="image.png",
        headers=Headers({"content-type": "image/png"}),
    )
    with Stubber(client) as stub:
        stub.add_response(
            "put_object",
            {},
            {
                "Bucket": "test-bucket",
                "Key": ANY,
                "Body": b"image-data",
                "ContentType": "image/png",
            },
        )
        path = await storage.save_image(image)
        assert path.startswith("/uploads/timeline/")
        assert not (tmp_path / "images").exists()
        key = "5history/" + path.removeprefix("/uploads/")
        stub.add_response("delete_object", {}, {"Bucket": "test-bucket", "Key": key})
        signed_url = object_storage.image_url(path.removeprefix("/uploads/"))
        assert "X-Amz-Signature=" in signed_url
        assert "5history/timeline/" in signed_url
        storage.delete_image(path)
        stub.assert_no_pending_responses()


@pytest.mark.parametrize(
    "path", ["../ukno/file.png", "/ukno/file.png", "foo/../../file", "foo\\bar"]
)
def test_s3_cannot_escape_prefix(path):
    with pytest.raises(ValueError):
        object_storage.object_key(path)


def test_local_delete_cannot_escape_storage(uploads_dir):
    tmp_path = uploads_dir
    outside = tmp_path / "outside.png"
    outside.write_bytes(b"keep")
    storage = ImageStorage(tmp_path / "images", "/uploads/timeline")
    storage.delete_image("/uploads/timeline/../outside.png")
    assert outside.read_bytes() == b"keep"
