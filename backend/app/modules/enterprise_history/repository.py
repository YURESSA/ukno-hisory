from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.enterprise_history.models import (
    EnterpriseHistory,
    EnterpriseHistoryGalleryImage,
    EnterpriseHistorySlide,
)


class EnterpriseHistoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, item: EnterpriseHistory):
        self.session.add(item)
        await self.session.commit()
        return await self.get_by_id(item.id, include_drafts=True)

    async def get_public_all(self):
        result = await self.session.execute(
            select(EnterpriseHistory)
            .where(EnterpriseHistory.is_draft.is_(False))
            .order_by(EnterpriseHistory.id.desc())
        )
        return result.scalars().all()

    async def get_all(self):
        result = await self.session.execute(
            select(EnterpriseHistory).order_by(EnterpriseHistory.id.desc())
        )
        return result.scalars().all()

    async def get_by_id(self, item_id: int, include_drafts: bool = False):
        query = (
            select(EnterpriseHistory)
            .options(
                selectinload(EnterpriseHistory.how_it_was_slides),
                selectinload(EnterpriseHistory.gallery_images),
            )
            .where(EnterpriseHistory.id == item_id)
            .execution_options(populate_existing=True)
        )
        if not include_drafts:
            query = query.where(EnterpriseHistory.is_draft.is_(False))

        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def delete(self, item: EnterpriseHistory):
        await self.session.delete(item)
        await self.session.commit()

    async def add_slides(self, slides: list[EnterpriseHistorySlide]):
        self.session.add_all(slides)

    async def add_gallery_images(self, images: list[EnterpriseHistoryGalleryImage]):
        self.session.add_all(images)
