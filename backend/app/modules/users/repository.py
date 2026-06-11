from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.models import User, UserRole


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User):
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_by_email(self, email: str):
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: int):
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_all(self):
        result = await self.session.execute(select(User))
        return result.scalars().all()

    async def get_total_count(self) -> int:
        result = await self.session.execute(select(func.count(User.id)))
        return int(result.scalar_one() or 0)

    async def get_role_count(self, role: UserRole | str) -> int:
        normalized_role = UserRole.normalize(role)
        result = await self.session.execute(
            select(func.count(User.id)).where(User.role == normalized_role)
        )
        return int(result.scalar_one() or 0)

    async def delete(self, user: User):
        await self.session.delete(user)
        await self.session.commit()
