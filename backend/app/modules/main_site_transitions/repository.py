from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.main_site_transitions.models import MainSiteTransition


class MainSiteTransitionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, item: MainSiteTransition) -> MainSiteTransition:
        self.session.add(item)
        await self.session.commit()
        return item

    async def get_total_count(self) -> int:
        result = await self.session.execute(select(func.count(MainSiteTransition.id)))
        return int(result.scalar_one() or 0)

    async def get_unique_client_ip_count(self) -> int:
        result = await self.session.execute(
            select(func.count(func.distinct(MainSiteTransition.client_ip))).where(
                MainSiteTransition.client_ip.is_not(None)
            )
        )
        return int(result.scalar_one() or 0)

    async def get_latest(self) -> MainSiteTransition | None:
        result = await self.session.execute(
            select(MainSiteTransition).order_by(
                MainSiteTransition.created_at.desc(),
                MainSiteTransition.id.desc(),
            )
        )
        return result.scalars().first()
