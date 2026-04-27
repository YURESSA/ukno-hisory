from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.student_projects.models import (
    StudentProject,
    StudentProjectGalleryImage,
)


class StudentProjectRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, project: StudentProject):
        self.session.add(project)
        await self.session.commit()
        return await self.get_by_id(project.id, include_drafts=True)

    async def get_public_all(self):
        result = await self.session.execute(
            select(StudentProject)
            .where(StudentProject.is_draft.is_(False))
            .order_by(StudentProject.id.desc())
        )
        return result.scalars().all()

    async def get_all(self):
        result = await self.session.execute(
            select(StudentProject).order_by(StudentProject.id.desc())
        )
        return result.scalars().all()

    async def get_by_id(self, project_id: int, include_drafts: bool = False):
        query = (
            select(StudentProject)
            .options(selectinload(StudentProject.gallery_images))
            .where(StudentProject.id == project_id)
            .execution_options(populate_existing=True)
        )
        if not include_drafts:
            query = query.where(StudentProject.is_draft.is_(False))

        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def delete(self, project: StudentProject):
        await self.session.delete(project)
        await self.session.commit()

    async def add_gallery_images(self, images: list[StudentProjectGalleryImage]):
        self.session.add_all(images)
