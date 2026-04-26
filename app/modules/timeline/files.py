from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status

from app.core.config import settings

ALLOWED_IMAGE_TYPES = {
    "image/gif": ".gif",
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


class TimelineFileStorage:
    def __init__(self):
        self.base_dir = Path(settings.UPLOAD_DIR)
        self.timeline_dir = self.base_dir / "timeline"
        self.timeline_dir.mkdir(parents=True, exist_ok=True)

    async def save_image(self, image: UploadFile) -> str:
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

        extension = ALLOWED_IMAGE_TYPES[image.content_type]
        filename = f"{uuid4().hex}{extension}"
        target = self.timeline_dir / filename
        target.write_bytes(content)

        return f"{settings.UPLOAD_URL_PREFIX}/timeline/{filename}"

    def delete_image(self, image_path: str | None) -> None:
        if not image_path:
            return

        prefix = f"{settings.UPLOAD_URL_PREFIX}/timeline/"
        if not image_path.startswith(prefix):
            return

        filename = image_path.removeprefix(prefix)
        target = self.timeline_dir / filename
        if target.exists():
            target.unlink()
