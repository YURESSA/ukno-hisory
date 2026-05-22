from app.common.file_storage import ImageStorage
from app.core.config import settings


class QuizFileStorage:
    def __init__(self):
        self.base_dir = settings.upload_dir_path
        self.quiz_dir = self.base_dir / "quiz"
        self.storage = ImageStorage(
            self.quiz_dir,
            f"{settings.UPLOAD_URL_PREFIX}/quiz",
        )

    async def save_image(self, image) -> str:
        return await self.storage.save_image(image)

    def delete_image(self, image_path: str | None) -> None:
        self.storage.delete_image(image_path)
