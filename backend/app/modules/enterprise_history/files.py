from app.common.file_storage import ImageStorage
from app.core.config import settings


class EnterpriseHistoryFileStorage:
    def __init__(self):
        self.base_dir = settings.upload_dir_path / "enterprise_history"
        self.general_main_dir = self.base_dir / "general_main"
        self.detail_main_dir = self.base_dir / "detail_main"
        self.how_it_was_dir = self.base_dir / "how_it_was"
        self.gallery_dir = self.base_dir / "gallery"
        self.storage = ImageStorage(
            self.base_dir,
            f"{settings.UPLOAD_URL_PREFIX}/enterprise_history",
        )

    async def save_general_main_image(self, image) -> str:
        return await self.storage.save_image(image, self.general_main_dir)

    async def save_detail_main_image(self, image) -> str:
        return await self.storage.save_image(image, self.detail_main_dir)

    async def save_how_it_was_image(self, image) -> str:
        return await self.storage.save_image(image, self.how_it_was_dir)

    async def save_gallery_image(self, image) -> str:
        return await self.storage.save_image(image, self.gallery_dir)

    def delete_image(self, image_path: str | None) -> None:
        self.storage.delete_image(image_path)
