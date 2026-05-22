from fastapi import APIRouter

from app.modules.auth.router import router as auth_router
from app.modules.enterprise_history.router import router as enterprise_history_router
from app.modules.quiz.router import router as quiz_router
from app.modules.student_projects.router import router as student_projects_router
from app.modules.timeline.router import router as timeline_router
from app.modules.users.router import router as users_router

router = APIRouter()

router.include_router(
    enterprise_history_router,
    prefix="/enterprise-history",
    tags=["История предприятий"],
)
router.include_router(
    student_projects_router,
    prefix="/student-projects",
    tags=["Студенческие проекты"],
)
router.include_router(users_router, prefix="/users", tags=["Пользователи"])
router.include_router(timeline_router, prefix="/timeline", tags=["Таймлайн"])
router.include_router(quiz_router, prefix="/quiz", tags=["Квиз"])
router.include_router(
    auth_router,
    prefix="/auth",
    tags=["Авторизация"],
    include_in_schema=False,
)
