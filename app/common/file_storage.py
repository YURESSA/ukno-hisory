from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status

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
        self.base_dir.mkdir(parents=True, exist_ok=True)

    async def save_image(self, image: UploadFile, directory: Path | None = None) -> str:
        if image.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported image type",
            )

        content = await image.read()
        if not content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Image file is empty",
            )

        target_dir = directory or self.base_dir
        target_dir.mkdir(parents=True, exist_ok=True)

        extension = ALLOWED_IMAGE_TYPES[image.content_type]
        filename = f"{uuid4().hex}{extension}"
        target = target_dir / filename
        target.write_bytes(content)

        relative_path = target.relative_to(self.base_dir).as_posix()
        if relative_path == ".":
            relative_path = filename

        return f"{self.url_prefix}/{relative_path}".replace("//", "/")

    def delete_image(self, image_path: str | None) -> None:
        if not image_path or not image_path.startswith(f"{self.url_prefix}/"):
            return

        relative_path = image_path.removeprefix(f"{self.url_prefix}/")
        target = self.base_dir / relative_path
        if target.exists():
            target.unlink()
