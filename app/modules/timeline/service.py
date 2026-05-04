from fastapi import HTTPException, status

from app.modules.timeline.files import TimelineFileStorage
from app.modules.timeline.models import TimelineEntry
from app.modules.timeline.schemas import TimelineUpdate


class TimelineService:
    def __init__(self, repo, file_storage: TimelineFileStorage):
        self.repo = repo
        self.file_storage = file_storage

    async def create_entry(self, year: int, image, text: str):
        image_path = await self.file_storage.save_image(image)
        entry = TimelineEntry(year=year, image=image_path, text=text)
        return await self.repo.create(entry)

    async def get_entries(self):
        return await self.repo.get_all()

    async def get_entry(self, entry_id: int):
        entry = await self.repo.get_by_id(entry_id)

        if not entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Запись таймлайна не найдена",
            )

        return entry

    async def update_entry(
        self,
        entry_id: int,
        data: TimelineUpdate,
    ):
        entry = await self.get_entry(entry_id)

        if "year" in data.model_fields_set:
            entry.year = data.year

        if "text" in data.model_fields_set:
            entry.text = data.text

        await self.repo.session.commit()
        await self.repo.session.refresh(entry)

        return entry

    async def update_entry_image(self, entry_id: int, image):
        entry = await self.get_entry(entry_id)

        old_image = entry.image
        image_path = await self.file_storage.save_image(image)
        entry.image = image_path

        await self.repo.session.commit()
        await self.repo.session.refresh(entry)

        if old_image is not None:
            self.file_storage.delete_image(old_image)

        return entry

    async def delete_entry_image(self, entry_id: int):
        entry = await self.get_entry(entry_id)
        image_path = entry.image
        entry.image = ""

        await self.repo.session.commit()
        await self.repo.session.refresh(entry)

        if image_path:
            self.file_storage.delete_image(image_path)

        return entry

    async def delete_entry(self, entry_id: int):
        entry = await self.get_entry(entry_id)
        image_path = entry.image
        await self.repo.delete(entry)
        self.file_storage.delete_image(image_path)
