from fastapi import HTTPException, status

from app.modules.timeline.files import TimelineFileStorage
from app.modules.timeline.models import TimelineEntry


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
                detail="Timeline entry not found",
            )

        return entry

    async def update_entry(
        self,
        entry_id: int,
        year: int | None,
        image,
        text: str | None,
    ):
        entry = await self.get_entry(entry_id)

        if year is not None:
            entry.year = year

        if text is not None:
            entry.text = text

        if image is not None:
            old_image = entry.image
            image_path = await self.file_storage.save_image(image)
            entry.image = image_path
        else:
            old_image = None

        await self.repo.session.commit()
        await self.repo.session.refresh(entry)

        if old_image is not None:
            self.file_storage.delete_image(old_image)

        return entry

    async def delete_entry(self, entry_id: int):
        entry = await self.get_entry(entry_id)
        image_path = entry.image
        await self.repo.delete(entry)
        self.file_storage.delete_image(image_path)
