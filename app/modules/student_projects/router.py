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
    StudentProjectUpdate,
)
from app.modules.student_projects.service import StudentProjectService

router = APIRouter()


def get_service(db=Depends(get_db)):
    return StudentProjectService(
        StudentProjectRepository(db),
        StudentProjectFileStorage(),
    )


@router.get(
    "",
    response_model=list[StudentProjectSummaryRead],
    summary="Получить список опубликованных студенческих проектов",
)
async def get_student_projects(service=Depends(get_service)):
    return await service.get_public_projects()


@router.get(
    "/admin",
    response_model=list[StudentProjectAdminSummaryRead],
    summary="Получить список студенческих проектов для администратора",
)
async def get_admin_student_projects(
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.get_admin_projects()


@router.get(
    "/{project_id}",
    response_model=StudentProjectDetailRead,
    summary="Получить опубликованный студенческий проект по идентификатору",
)
async def get_student_project(project_id: int, service=Depends(get_service)):
    return await service.get_public_project(project_id)


@router.get(
    "/admin/{project_id}",
    response_model=StudentProjectAdminDetailRead,
    summary="Получить студенческий проект по идентификатору для администратора",
)
async def get_admin_student_project(
    project_id: int,
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.get_admin_project(project_id)


@router.post(
    "",
    response_model=StudentProjectAdminDetailRead,
    status_code=201,
    summary="Создать студенческий проект",
)
async def create_student_project(
    title: str | None = Form(None),
    author: str | None = Form(None),
    short_description: str | None = Form(None),
    description: str | None = Form(None),
    year: int | None = Form(None, ge=1),
    tag_one: str | None = Form(None),
    tag_two: str | None = Form(None),
    is_draft: bool = Form(True),
    main_image: UploadFile | None = File(None),
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


@router.patch(
    "/{project_id}",
    response_model=StudentProjectAdminDetailRead,
    summary="Обновить данные студенческого проекта",
)
async def update_student_project(
    project_id: int,
    data: StudentProjectUpdate,
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    if not data.model_fields_set:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Для обновления нужно передать хотя бы одно поле",
        )

    return await service.update_project(project_id, data=data)


@router.put(
    "/{project_id}/main-image",
    response_model=StudentProjectAdminDetailRead,
    summary="Загрузить или заменить главную картинку студенческого проекта",
)
async def update_student_project_main_image(
    project_id: int,
    main_image: UploadFile = File(...),
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.update_main_image(project_id, main_image)


@router.delete(
    "/{project_id}/main-image",
    response_model=StudentProjectAdminDetailRead,
    summary="Удалить главную картинку студенческого проекта",
)
async def delete_student_project_main_image(
    project_id: int,
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.delete_main_image(project_id)


@router.post(
    "/{project_id}/gallery",
    response_model=StudentProjectAdminDetailRead,
    status_code=status.HTTP_200_OK,
    summary="Добавить изображения в галерею студенческого проекта",
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
    summary="Удалить изображение из галереи студенческого проекта",
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
    summary="Изменить порядок изображений в галерее студенческого проекта",
)
async def reorder_student_project_gallery(
    project_id: int,
    data: StudentProjectGalleryOrderUpdate,
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.reorder_gallery(project_id, data.image_ids)


@router.delete(
    "/{project_id}",
    summary="Удалить студенческий проект",
)
async def delete_student_project(
    project_id: int,
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    await service.delete_project(project_id)
    return {"detail": "Студенческий проект удалён"}
