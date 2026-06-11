from fastapi import HTTPException, status

from app.modules.subdistricts.constants import (
    SUBDISTRICT_NAMES,
    normalize_subdistrict_name,
)
from app.modules.subdistricts.files import SubdistrictFileStorage
from app.modules.subdistricts.schemas import (
    SubdistrictDetailRead,
    SubdistrictEnterpriseRead,
    SubdistrictPopularityRead,
    SubdistrictPopularStatsRead,
    SubdistrictRead,
)


class SubdistrictService:
    def __init__(self, repo, file_storage: SubdistrictFileStorage):
        self.repo = repo
        self.file_storage = file_storage

    async def get_all(self) -> list[SubdistrictRead]:
        items: list[SubdistrictRead] = []
        for name in SUBDISTRICT_NAMES:
            content = await self.repo.get_content(name)
            items.append(
                SubdistrictRead(
                    name=name,
                    description=content.description if content else None,
                    image=content.image if content else None,
                )
            )
        return items

    async def get_detail(self, subdistrict_name: str) -> SubdistrictDetailRead:
        name = self._normalize_or_404(subdistrict_name)
        content = await self.repo.increment_views(name)
        enterprises = await self.repo.get_public_enterprises(name)
        return SubdistrictDetailRead(
            name=name,
            description=content.description if content else None,
            image=content.image if content else None,
            enterprises=[
                SubdistrictEnterpriseRead(id=item.id, title=item.title or "")
                for item in enterprises
            ],
        )

    async def get_popular_stats(self) -> SubdistrictPopularStatsRead:
        existing_items = {
            item.name: item for item in await self.repo.get_popularity_items()
        }
        items = [
            SubdistrictPopularityRead(
                name=name,
                views_count=(
                    existing_items.get(name).views_count
                    if existing_items.get(name) is not None
                    else 0
                ),
            )
            for name in SUBDISTRICT_NAMES
        ]
        items.sort(key=lambda item: (-item.views_count, item.name))
        most_popular = items[0] if items and items[0].views_count > 0 else None
        return SubdistrictPopularStatsRead(
            most_popular=most_popular,
            items=items,
        )

    async def update_content(self, subdistrict_name: str, *, description: str | None):
        name = self._normalize_or_404(subdistrict_name)
        content = await self.repo.get_or_create_content(name)
        content.description = self._clean_text(description)
        await self.repo.session.commit()
        return await self.get_detail(name)

    async def update_image(self, subdistrict_name: str, image):
        name = self._normalize_or_404(subdistrict_name)
        content = await self.repo.get_or_create_content(name)
        old_image = content.image
        content.image = await self.file_storage.save_image(image)
        await self.repo.session.commit()
        if old_image is not None:
            self.file_storage.delete_image(old_image)
        return await self.get_detail(name)

    async def delete_image(self, subdistrict_name: str):
        name = self._normalize_or_404(subdistrict_name)
        content = await self.repo.get_or_create_content(name)
        old_image = content.image
        content.image = None
        await self.repo.session.commit()
        if old_image is not None:
            self.file_storage.delete_image(old_image)
        return await self.get_detail(name)

    def _normalize_or_404(self, value: str) -> str:
        try:
            return normalize_subdistrict_name(value)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Подрайон не найден",
            ) from exc

    def _clean_text(self, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        return cleaned or None
