from asyncio import to_thread
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status

from app.common import object_storage
from app.core.config import settings

ALLOWED_IMAGE_TYPES = {
    "image/gif": ".gif",
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


class ImageStorage:
    def __init__(self, base_dir: Path, url_prefix: str):
        self.base_dir = base_dir
        self.url_prefix = url_prefix.rstrip("/")
        if settings.STORAGE_BACKEND == "local":
            self.base_dir.mkdir(parents=True, exist_ok=True)

    async def save_image(self, image: UploadFile, directory: Path | None = None) -> str:
        if image.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Неподдерживаемый формат изображения",
            )

        content = await image.read()
        if not content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Файл изображения пуст",
            )

        target_dir = directory or self.base_dir

        extension = ALLOWED_IMAGE_TYPES[image.content_type]
        filename = f"{uuid4().hex}{extension}"
        target = target_dir / filename

        relative_path = target.relative_to(self.base_dir).as_posix()
        if relative_path == ".":
            relative_path = filename

        if settings.STORAGE_BACKEND == "s3":
            folder = self.url_prefix.removeprefix(settings.UPLOAD_URL_PREFIX).strip("/")
            storage_path = f"{folder}/{relative_path}"
            await to_thread(
                object_storage.put_image, storage_path, content, image.content_type
            )
        else:
            target_dir.mkdir(parents=True, exist_ok=True)
            await to_thread(target.write_bytes, content)

        return f"{self.url_prefix}/{relative_path}".replace("//", "/")

    def delete_image(self, image_path: str | None) -> None:
        if not image_path or not image_path.startswith(f"{self.url_prefix}/"):
            return

        relative_path = image_path.removeprefix(f"{self.url_prefix}/")
        target = (self.base_dir / relative_path).resolve()
        if not target.is_relative_to(self.base_dir.resolve()) or "\\" in relative_path:
            return
        if settings.STORAGE_BACKEND == "s3":
            storage_path = image_path.removeprefix(f"{settings.UPLOAD_URL_PREFIX}/")
            object_storage.delete_image(storage_path)
            return
        if target.exists():
            target.unlink()
