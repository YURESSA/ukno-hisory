from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from app.core.database import get_db
from app.core.dependencies import require_admin
from app.modules.student_projects.files import StudentProjectFileStorage
from app.modules.student_projects.repository import StudentProjectRepository
from app.modules.student_projects.schemas import (
    StudentProjectAdminDetailRead,
    StudentProjectAdminSummaryRead,
    StudentProjectDetailRead,
    StudentProjectGalleryOrderUpdate,
    StudentProjectSummaryRead,
)
from app.modules.student_projects.service import StudentProjectService

router = APIRouter()


def get_service(db=Depends(get_db)):
    return StudentProjectService(
        StudentProjectRepository(db),
        StudentProjectFileStorage(),
    )


@router.get("", response_model=list[StudentProjectSummaryRead])
async def get_student_projects(service=Depends(get_service)):
    return await service.get_public_projects()


@router.get("/admin", response_model=list[StudentProjectAdminSummaryRead])
async def get_admin_student_projects(
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.get_admin_projects()


@router.get("/{project_id}", response_model=StudentProjectDetailRead)
async def get_student_project(project_id: int, service=Depends(get_service)):
    return await service.get_public_project(project_id)


@router.get("/admin/{project_id}", response_model=StudentProjectAdminDetailRead)
async def get_admin_student_project(
    project_id: int,
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.get_admin_project(project_id)


@router.post("", response_model=StudentProjectAdminDetailRead, status_code=201)
async def create_student_project(
    title: Annotated[str | None, Form()] = None,
    author: Annotated[str | None, Form()] = None,
    short_description: Annotated[str | None, Form()] = None,
    description: Annotated[str | None, Form()] = None,
    year: Annotated[int | None, Form(ge=1)] = None,
    tag_one: Annotated[str | None, Form()] = None,
    tag_two: Annotated[str | None, Form()] = None,
    is_draft: bool = Form(True),
    main_image: Annotated[UploadFile | None, File()] = None,
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.create_project(
        title=title,
        author=author,
        short_description=short_description,
        description=description,
        year=year,
        tag_one=tag_one,
        tag_two=tag_two,
        is_draft=is_draft,
        main_image=main_image,
    )


@router.put("/{project_id}", response_model=StudentProjectAdminDetailRead)
async def update_student_project(
    project_id: int,
    title: Annotated[str | None, Form()] = None,
    author: Annotated[str | None, Form()] = None,
    short_description: Annotated[str | None, Form()] = None,
    description: Annotated[str | None, Form()] = None,
    year: Annotated[int | None, Form(ge=1)] = None,
    clear_year: bool = Form(False),
    tag_one: Annotated[str | None, Form()] = None,
    tag_two: Annotated[str | None, Form()] = None,
    is_draft: Annotated[bool | None, Form()] = None,
    remove_main_image: bool = Form(False),
    main_image: Annotated[UploadFile | None, File()] = None,
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    if (
        title is None
        and author is None
        and short_description is None
        and description is None
        and year is None
        and not clear_year
        and tag_one is None
        and tag_two is None
        and is_draft is None
        and not remove_main_image
        and main_image is None
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="At least one field must be provided for update",
        )

    return await service.update_project(
        project_id,
        title=title,
        author=author,
        short_description=short_description,
        description=description,
        year=year,
        clear_year=clear_year,
        tag_one=tag_one,
        tag_two=tag_two,
        is_draft=is_draft,
        main_image=main_image,
        remove_main_image=remove_main_image,
    )


@router.post(
    "/{project_id}/gallery",
    response_model=StudentProjectAdminDetailRead,
    status_code=status.HTTP_200_OK,
    openapi_extra={
        "requestBody": {
            "required": True,
            "content": {
                "multipart/form-data": {
                    "schema": {
                        "type": "object",
                        "required": ["images"],
                        "properties": {
                            "images": {
                                "type": "array",
                                "items": {
                                    "type": "string",
                                    "format": "binary",
                                },
                            }
                        },
                    }
                }
            },
        }
    },
)
async def add_student_project_gallery_image(
    project_id: int,
    images: list[UploadFile] = File(...),
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    project = await service.add_gallery_images(project_id, images)
    return service._build_admin_detail(project)


@router.delete(
    "/{project_id}/gallery/{image_id}",
    response_model=StudentProjectAdminDetailRead,
)
async def delete_student_project_gallery_image(
    project_id: int,
    image_id: int,
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.delete_gallery_image(project_id, image_id)


@router.put(
    "/{project_id}/gallery/order",
    response_model=StudentProjectAdminDetailRead,
)
async def reorder_student_project_gallery(
    project_id: int,
    data: StudentProjectGalleryOrderUpdate,
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.reorder_gallery(project_id, data.image_ids)


@router.delete("/{project_id}")
async def delete_student_project(
    project_id: int,
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    await service.delete_project(project_id)
    return {"detail": "Student project deleted"}
