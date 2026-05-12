from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.timeline.models import TimelineEntry


class TimelineRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, entry: TimelineEntry):
        self.session.add(entry)
        await self.session.commit()
        await self.session.refresh(entry)
        return entry

    async def get_all(self):
        result = await self.session.execute(
            select(TimelineEntry)
            .where(TimelineEntry.year >= 1)
            .order_by(
                TimelineEntry.year.asc(),
                TimelineEntry.id.asc(),
            )
        )
        return result.scalars().all()

    async def get_by_id(self, entry_id: int):
        result = await self.session.execute(
            select(TimelineEntry).where(
                TimelineEntry.id == entry_id,
                TimelineEntry.year >= 1,
            )
        )
        return result.scalar_one_or_none()

    async def delete(self, entry: TimelineEntry):
        await self.session.delete(entry)
        await self.session.commit()
