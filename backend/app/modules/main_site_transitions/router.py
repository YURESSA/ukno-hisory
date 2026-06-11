from fastapi import APIRouter, Depends, Request, status

from app.core.database import get_db
from app.core.dependencies import require_admin
from app.modules.main_site_transitions.repository import (
    MainSiteTransitionRepository,
)
from app.modules.main_site_transitions.schemas import MainSiteTransitionRead
from app.modules.main_site_transitions.service import MainSiteTransitionService

router = APIRouter()


def get_service(db=Depends(get_db)):
    return MainSiteTransitionService(MainSiteTransitionRepository(db))


def _get_client_ip(request: Request) -> str | None:
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip() or None

    return request.client.host if request.client else None


@router.post(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Зафиксировать переход на основной сайт",
)
async def track_main_site_transition(
    request: Request,
    service=Depends(get_service),
):
    client_ip = _get_client_ip(request)
    user_agent = request.headers.get("user-agent")
    await service.track_transition(
        client_ip=client_ip,
        user_agent=user_agent,
    )


@router.get(
    "/stats",
    response_model=MainSiteTransitionRead,
    status_code=status.HTTP_200_OK,
    summary="Получить количество переходов на основной сайт",
)
async def get_main_site_transition_stats(
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.get_stats()
