from pathlib import Path

from app.common.file_storage import ImageStorage
from app.core.config import settings


class TimelineFileStorage:
    def __init__(self):
        self.base_dir = Path(settings.UPLOAD_DIR)
        self.timeline_dir = self.base_dir / "timeline"
        self.storage = ImageStorage(
            self.timeline_dir,
            f"{settings.UPLOAD_URL_PREFIX}/timeline",
        )

    async def save_image(self, image) -> str:
        return await self.storage.save_image(image)

    def delete_image(self, image_path: str | None) -> None:
        self.storage.delete_image(image_path)
