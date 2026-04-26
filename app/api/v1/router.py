from fastapi import APIRouter

from app.modules.auth.router import router as auth_router
from app.modules.timeline.router import router as timeline_router
from app.modules.users.router import router as users_router

router = APIRouter()

router.include_router(users_router, prefix="/users", tags=["Users"])
router.include_router(timeline_router, prefix="/timeline", tags=["Timeline"])
router.include_router(
    auth_router, prefix="/auth", tags=["Auth"], include_in_schema=False
)
