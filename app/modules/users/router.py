from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserCreate, UserRead
from app.modules.users.service import UserService

router = APIRouter()


def get_service(db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    return UserService(repo)


@router.post("/", response_model=UserRead)
async def create_user(
    data: UserCreate,
    service: UserService = Depends(get_service),
):
    return await service.create_user(data.name)


@router.get("/", response_model=list[UserRead])
async def get_users(
    service: UserService = Depends(get_service),
):
    return await service.get_users()
