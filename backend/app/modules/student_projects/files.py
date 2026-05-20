from app.common.file_storage import ImageStorage
from app.core.config import settings


class StudentProjectFileStorage:
    def __init__(self):
        self.base_dir = settings.upload_dir_path / "student_projects"
        self.main_dir = self.base_dir / "main"
        self.gallery_dir = self.base_dir / "gallery"
        self.storage = ImageStorage(
            self.base_dir,
            f"{settings.UPLOAD_URL_PREFIX}/student_projects",
        )

    async def save_main_image(self, image) -> str:
        return await self.storage.save_image(image, self.main_dir)

    async def save_gallery_image(self, image) -> str:
        return await self.storage.save_image(image, self.gallery_dir)

    def delete_image(self, image_path: str | None) -> None:
        self.storage.delete_image(image_path)
