from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.enterprise_history.models import EnterpriseHistory
from app.modules.subdistricts.models import SubdistrictContent


class SubdistrictRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_content(self, name: str) -> SubdistrictContent | None:
        return await self.session.get(SubdistrictContent, name)

    async def get_or_create_content(self, name: str) -> SubdistrictContent:
        content = await self.get_content(name)
        if content is not None:
            return content

        content = SubdistrictContent(name=name)
        self.session.add(content)
        await self.session.flush()
        return content

    async def increment_views(self, name: str) -> SubdistrictContent:
        content = await self.get_or_create_content(name)
        content.views_count += 1
        await self.session.commit()
        await self.session.refresh(content)
        return content

    async def get_popularity_items(self) -> list[SubdistrictContent]:
        result = await self.session.execute(
            select(SubdistrictContent).order_by(
                SubdistrictContent.views_count.desc(),
                SubdistrictContent.name.asc(),
            )
        )
        return result.scalars().all()

    async def get_public_enterprises(self, name: str) -> list[EnterpriseHistory]:
        result = await self.session.execute(
            select(EnterpriseHistory)
            .where(
                EnterpriseHistory.subdistrict == name,
                EnterpriseHistory.is_draft.is_(False),
            )
            .order_by(EnterpriseHistory.id.desc())
        )
        return result.scalars().all()
