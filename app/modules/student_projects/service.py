from fastapi import HTTPException, status

from app.modules.student_projects.files import StudentProjectFileStorage
from app.modules.student_projects.models import (
    StudentProject,
    StudentProjectGalleryImage,
)
from app.modules.student_projects.schemas import (
    StudentProjectAdminDetailRead,
    StudentProjectDetailRead,
    StudentProjectTagRead,
    StudentProjectUpdate,
)


class StudentProjectService:
    def __init__(self, repo, file_storage: StudentProjectFileStorage):
        self.repo = repo
        self.file_storage = file_storage

    async def create_project(
        self,
        *,
        title: str | None,
        author: str | None,
        short_description: str | None,
        description: str | None,
        year: int | None,
        tag_one: str | None,
        tag_two: str | None,
        is_draft: bool,
        main_image,
    ):
        main_image_path = None
        if main_image is not None:
            main_image_path = await self.file_storage.save_main_image(main_image)

        project = StudentProject(
            title=self._clean_text(title),
            author=self._clean_text(author),
            short_description=self._clean_text(short_description),
            description=self._clean_text(description),
            main_image=main_image_path,
            year=year,
            tag_one=self._clean_text(tag_one),
            tag_two=self._clean_text(tag_two),
            is_draft=is_draft,
        )

        self._validate_publishable(project, is_draft)
        project = await self.repo.create(project)
        return self._build_admin_detail(project)

    async def get_public_projects(self):
        return await self.repo.get_public_all()

    async def get_admin_projects(self):
        return await self.repo.get_all()

    async def get_public_project(self, project_id: int):
        project = await self.repo.get_by_id(project_id, include_drafts=False)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Студенческий проект не найден",
            )
        return self._build_public_detail(project)

    async def get_admin_project(self, project_id: int):
        project = await self.repo.get_by_id(project_id, include_drafts=True)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Студенческий проект не найден",
            )
        return self._build_admin_detail(project)

    async def update_project(
        self,
        project_id: int,
        *,
        data: StudentProjectUpdate,
    ):
        project = await self.repo.get_by_id(project_id, include_drafts=True)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Студенческий проект не найден",
            )

        text_fields = (
            "title",
            "author",
            "short_description",
            "description",
            "tag_one",
            "tag_two",
        )
        for field in text_fields:
            if field in data.model_fields_set:
                setattr(project, field, self._clean_text(getattr(data, field)))

        if "year" in data.model_fields_set:
            project.year = data.year

        if "is_draft" in data.model_fields_set:
            project.is_draft = data.is_draft

        self._validate_publishable(project, project.is_draft)
        await self.repo.session.commit()
        await self.repo.session.refresh(project)
        project = await self.repo.get_by_id(project.id, include_drafts=True)

        return self._build_admin_detail(project)

    async def update_main_image(self, project_id: int, main_image):
        project = await self.repo.get_by_id(project_id, include_drafts=True)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Студенческий проект не найден",
            )

        old_main_image = project.main_image
        project.main_image = await self.file_storage.save_main_image(main_image)

        self._validate_publishable(project, project.is_draft)
        await self.repo.session.commit()
        await self.repo.session.refresh(project)
        project = await self.repo.get_by_id(project.id, include_drafts=True)

        if old_main_image is not None:
            self.file_storage.delete_image(old_main_image)

        return self._build_admin_detail(project)

    async def add_gallery_images(self, project_id: int, images: list):
        project = await self.repo.get_by_id(project_id, include_drafts=True)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Студенческий проект не найден",
            )

        start_position = len(project.gallery_images)
        for offset, image in enumerate(images):
            image_path = await self.file_storage.save_gallery_image(image)
            gallery_item = StudentProjectGalleryImage(
                project_id=project.id,
                image=image_path,
                position=start_position + offset,
            )
            self.repo.session.add(gallery_item)

        await self.repo.session.commit()
        return await self.repo.get_by_id(project.id, include_drafts=True)

    async def delete_main_image(self, project_id: int):
        project = await self.repo.get_by_id(project_id, include_drafts=True)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Студенческий проект не найден",
            )

        image_path = project.main_image
        project.main_image = None

        await self.repo.session.commit()
        await self.repo.session.refresh(project)
        project = await self.repo.get_by_id(project.id, include_drafts=True)

        if image_path is not None:
            self.file_storage.delete_image(image_path)

        return self._build_admin_detail(project)

    async def delete_gallery_image(self, project_id: int, image_id: int):
        project = await self.repo.get_by_id(project_id, include_drafts=True)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Студенческий проект не найден",
            )

        target = next(
            (item for item in project.gallery_images if item.id == image_id),
            None,
        )
        if not target:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Изображение галереи не найдено",
            )

        image_path = target.image
        await self.repo.session.delete(target)
        project.gallery_images = [
            item for item in project.gallery_images if item.id != image_id
        ]
        self._reorder_gallery(project)
        await self.repo.session.commit()
        self.file_storage.delete_image(image_path)
        project = await self.repo.get_by_id(project.id, include_drafts=True)
        return self._build_admin_detail(project)

    async def reorder_gallery(self, project_id: int, image_ids: list[int]):
        project = await self.repo.get_by_id(project_id, include_drafts=True)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Студенческий проект не найден",
            )

        current_ids = [item.id for item in project.gallery_images]
        if sorted(current_ids) != sorted(image_ids):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=(
                    "Порядок галереи должен содержать все текущие "
                    "идентификаторы изображений без пропусков и дубликатов"
                ),
            )

        mapping = {item.id: item for item in project.gallery_images}
        ordered = [mapping[item_id] for item_id in image_ids]
        for position, item in enumerate(ordered):
            item.position = position

        project.gallery_images = ordered
        await self.repo.session.commit()
        project = await self.repo.get_by_id(project.id, include_drafts=True)
        return self._build_admin_detail(project)

    async def delete_project(self, project_id: int):
        project = await self.repo.get_by_id(project_id, include_drafts=True)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Студенческий проект не найден",
            )

        image_paths = []
        if project.main_image:
            image_paths.append(project.main_image)
        image_paths.extend(item.image for item in project.gallery_images)

        await self.repo.delete(project)
        for image_path in image_paths:
            self.file_storage.delete_image(image_path)

    def _validate_publishable(self, project: StudentProject, is_draft: bool):
        if is_draft:
            return

        required_fields = {
            "title": project.title,
            "author": project.author,
            "short_description": project.short_description,
            "description": project.description,
            "main_image": project.main_image,
            "year": project.year,
        }
        missing_fields = [key for key, value in required_fields.items() if not value]

        if missing_fields:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=(
                    "Черновик нельзя опубликовать без обязательных полей: "
                    + ", ".join(missing_fields)
                ),
            )

    def _build_public_detail(self, project: StudentProject) -> StudentProjectDetailRead:
        return StudentProjectDetailRead(
            id=project.id,
            title=project.title or "",
            main_image=project.main_image or "",
            description=project.description or "",
            tags=StudentProjectTagRead(
                author=project.author or "",
                year=project.year or 0,
                tag_one=project.tag_one,
                tag_two=project.tag_two,
            ),
            gallery=project.gallery_images,
        )

    def _build_admin_detail(
        self,
        project: StudentProject,
    ) -> StudentProjectAdminDetailRead:
        return StudentProjectAdminDetailRead(
            id=project.id,
            title=project.title,
            author=project.author,
            short_description=project.short_description,
            description=project.description,
            main_image=project.main_image,
            year=project.year,
            tag_one=project.tag_one,
            tag_two=project.tag_two,
            is_draft=project.is_draft,
            gallery=project.gallery_images,
        )

    def _apply_optional_text(
        self,
        project: StudentProject,
        field: str,
        value: str | None,
    ):
        if value is not None:
            setattr(project, field, self._clean_text(value))

    def _clean_text(self, value: str | None) -> str | None:
        if value is None:
            return None

        cleaned = value.strip()
        return cleaned or None

    def _reorder_gallery(self, project: StudentProject) -> None:
        for position, image in enumerate(project.gallery_images):
            image.position = position
