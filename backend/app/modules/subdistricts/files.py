from app.common.file_storage import ImageStorage
from app.core.config import settings


class SubdistrictFileStorage:
    def __init__(self):
        self.base_dir = settings.upload_dir_path / "subdistricts"
        self.image_dir = self.base_dir / "images"
        self.storage = ImageStorage(
            self.base_dir,
            f"{settings.UPLOAD_URL_PREFIX}/subdistricts",
        )

    async def save_image(self, image) -> str:
        return await self.storage.save_image(image, self.image_dir)

    def delete_image(self, image_path: str | None) -> None:
        self.storage.delete_image(image_path)
