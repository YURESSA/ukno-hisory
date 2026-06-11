from app.modules.main_site_transitions.models import MainSiteTransition
from app.modules.main_site_transitions.schemas import MainSiteTransitionRead


class MainSiteTransitionService:
    def __init__(self, repo):
        self.repo = repo

    async def track_transition(
        self,
        *,
        client_ip: str | None,
        user_agent: str | None,
    ) -> MainSiteTransitionRead:
        item = MainSiteTransition(
            client_ip=client_ip,
            user_agent=user_agent,
        )
        await self.repo.create(item)
        return await self.get_stats()

    async def get_stats(self) -> MainSiteTransitionRead:
        total_count = await self.repo.get_total_count()
        latest = await self.repo.get_latest()
        return MainSiteTransitionRead(
            total_count=total_count,
            latest_transition_at=(
                latest.created_at.isoformat() if latest is not None else None
            ),
        )
