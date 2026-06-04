from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.quiz.models import QuizAttempt, QuizQuestion


class QuizRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, item: QuizQuestion):
        self.session.add(item)
        await self.session.commit()
        return await self.get_by_id(item.id)

    async def get_all(self):
        result = await self.session.execute(
            select(QuizQuestion)
            .options(selectinload(QuizQuestion.options))
            .order_by(QuizQuestion.id.asc())
        )
        return result.scalars().all()

    async def get_by_id(self, item_id: int):
        result = await self.session.execute(
            select(QuizQuestion)
            .options(selectinload(QuizQuestion.options))
            .where(QuizQuestion.id == item_id)
            .execution_options(populate_existing=True)
        )
        return result.scalar_one_or_none()

    async def delete(self, item: QuizQuestion):
        await self.session.delete(item)
        await self.session.commit()

    async def create_attempt(self, item: QuizAttempt):
        self.session.add(item)
        await self.session.commit()
        return await self.get_attempt_by_id(item.id)

    async def get_attempt_by_id(self, item_id: int):
        result = await self.session.execute(
            select(QuizAttempt)
            .options(
                selectinload(QuizAttempt.answers),
            )
            .where(QuizAttempt.id == item_id)
            .execution_options(populate_existing=True)
        )
        return result.scalar_one_or_none()

    async def get_all_attempts(self):
        result = await self.session.execute(
            select(QuizAttempt)
            .options(selectinload(QuizAttempt.answers))
            .order_by(QuizAttempt.updated_at.desc(), QuizAttempt.id.desc())
        )
        return result.scalars().all()
