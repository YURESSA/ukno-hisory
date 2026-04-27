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
                detail="Student project not found",
            )
        return self._build_public_detail(project)

    async def get_admin_project(self, project_id: int):
        project = await self.repo.get_by_id(project_id, include_drafts=True)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student project not found",
            )
        return self._build_admin_detail(project)

    async def update_project(
        self,
        project_id: int,
        *,
        title: str | None,
        author: str | None,
        short_description: str | None,
        description: str | None,
        year: int | None,
        clear_year: bool,
        tag_one: str | None,
        tag_two: str | None,
        is_draft: bool | None,
        main_image,
        remove_main_image: bool,
    ):
        project = await self.repo.get_by_id(project_id, include_drafts=True)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student project not found",
            )

        self._apply_optional_text(project, "title", title)
        self._apply_optional_text(project, "author", author)
        self._apply_optional_text(project, "short_description", short_description)
        self._apply_optional_text(project, "description", description)
        self._apply_optional_text(project, "tag_one", tag_one)
        self._apply_optional_text(project, "tag_two", tag_two)

        if clear_year:
            project.year = None
        elif year is not None:
            project.year = year

        old_main_image = None
        if remove_main_image and project.main_image:
            old_main_image = project.main_image
            project.main_image = None

        if main_image is not None:
            if project.main_image:
                old_main_image = project.main_image
            project.main_image = await self.file_storage.save_main_image(main_image)

        if is_draft is not None:
            project.is_draft = is_draft

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
                detail="Student project not found",
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

    async def delete_gallery_image(self, project_id: int, image_id: int):
        project = await self.repo.get_by_id(project_id, include_drafts=True)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student project not found",
            )

        target = next(
            (item for item in project.gallery_images if item.id == image_id),
            None,
        )
        if not target:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Gallery image not found",
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
                detail="Student project not found",
            )

        current_ids = [item.id for item in project.gallery_images]
        if sorted(current_ids) != sorted(image_ids):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=(
                    "Gallery order must contain exactly all current "
                    "gallery image ids"
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
                detail="Student project not found",
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
                    "Draft cannot be published without required fields: "
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
