from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from app.core.database import get_db
from app.core.dependencies import require_admin
from app.modules.enterprise_history.files import EnterpriseHistoryFileStorage
from app.modules.enterprise_history.repository import EnterpriseHistoryRepository
from app.modules.enterprise_history.schemas import (
    EnterpriseHistoryAdminDetailRead,
    EnterpriseHistoryAdminSummaryRead,
    EnterpriseHistoryDetailRead,
    EnterpriseHistoryGalleryOrderUpdate,
    EnterpriseHistorySlideOrderUpdate,
    EnterpriseHistorySlideUpdate,
    EnterpriseHistorySummaryRead,
    EnterpriseHistoryUpdate,
)
from app.modules.enterprise_history.service import EnterpriseHistoryService

router = APIRouter()


def get_service(db=Depends(get_db)):
    return EnterpriseHistoryService(
        EnterpriseHistoryRepository(db),
        EnterpriseHistoryFileStorage(),
    )


@router.get(
    "",
    response_model=list[EnterpriseHistorySummaryRead],
    summary="Получить список опубликованных историй предприятий",
)
async def get_enterprise_histories(
    subdistrict: str | None = None,
    service=Depends(get_service),
):
    items = await service.get_public_items(subdistrict=subdistrict)
    return [
        EnterpriseHistorySummaryRead(
            id=item.id,
            title=item.title or "",
            subdistrict=item.subdistrict or "",
            subtitle=item.general_subtitle or "",
            short_description=item.short_description or "",
            main_image=item.general_main_image or "",
        )
        for item in items
    ]


@router.get(
    "/admin",
    response_model=list[EnterpriseHistoryAdminSummaryRead],
    summary="Получить список историй предприятий для администратора",
)
async def get_admin_enterprise_histories(
    subdistrict: str | None = None,
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.get_admin_items(subdistrict=subdistrict)


@router.get(
    "/{item_id}",
    response_model=EnterpriseHistoryDetailRead,
    summary="Получить опубликованную историю предприятия по идентификатору",
)
async def get_enterprise_history(item_id: int, service=Depends(get_service)):
    return await service.get_public_item(item_id)


@router.get(
    "/admin/{item_id}",
    response_model=EnterpriseHistoryAdminDetailRead,
    summary="Получить историю предприятия по идентификатору для администратора",
)
async def get_admin_enterprise_history(
    item_id: int,
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.get_admin_item(item_id)


@router.post(
    "",
    response_model=EnterpriseHistoryAdminDetailRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать историю предприятия",
    openapi_extra={
        "requestBody": {
            "content": {
                "multipart/form-data": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "subdistrict": {"type": "string"},
                            "general_subtitle": {"type": "string"},
                            "detail_subtitle": {"type": "string"},
                            "short_description": {"type": "string"},
                            "is_draft": {"type": "boolean", "default": True},
                            "general_main_image": {
                                "type": "string",
                                "format": "binary",
                            },
                            "detail_main_image": {
                                "type": "string",
                                "format": "binary",
                            },
                            "gallery": {
                                "type": "array",
                                "items": {"type": "string", "format": "binary"},
                            },
                        },
                    }
                }
            }
        }
    },
)
async def create_enterprise_history(
    title: str | None = Form(None),
    subdistrict: str | None = Form(None),
    general_subtitle: str | None = Form(None),
    detail_subtitle: str | None = Form(None),
    short_description: str | None = Form(None),
    is_draft: bool = Form(True),
    general_main_image: UploadFile | None = File(None),
    detail_main_image: UploadFile | None = File(None),
    gallery: list[UploadFile] | None = File(None),
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.create_item(
        title=title,
        subdistrict=subdistrict,
        general_subtitle=general_subtitle,
        detail_subtitle=detail_subtitle,
        short_description=short_description,
        is_draft=is_draft,
        general_main_image=general_main_image,
        detail_main_image=detail_main_image,
        gallery_images=gallery,
    )


@router.patch(
    "/{item_id}",
    response_model=EnterpriseHistoryAdminDetailRead,
    summary="Обновить данные истории предприятия",
)
async def update_enterprise_history(
    item_id: int,
    data: EnterpriseHistoryUpdate,
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    if not data.model_fields_set:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Для обновления нужно передать хотя бы одно поле",
        )
    return await service.update_item(item_id, data=data)


@router.put(
    "/{item_id}/general-main-image",
    response_model=EnterpriseHistoryAdminDetailRead,
    summary="Загрузить или заменить главное изображение общего блока",
)
async def update_enterprise_history_general_main_image(
    item_id: int,
    image: UploadFile = File(...),
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.update_general_main_image(item_id, image)


@router.delete(
    "/{item_id}/general-main-image",
    response_model=EnterpriseHistoryAdminDetailRead,
    summary="Удалить главное изображение общего блока",
)
async def delete_enterprise_history_general_main_image(
    item_id: int,
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.delete_general_main_image(item_id)


@router.put(
    "/{item_id}/detail-main-image",
    response_model=EnterpriseHistoryAdminDetailRead,
    summary="Загрузить или заменить главное изображение детального блока",
)
async def update_enterprise_history_detail_main_image(
    item_id: int,
    image: UploadFile = File(...),
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.update_detail_main_image(item_id, image)


@router.delete(
    "/{item_id}/detail-main-image",
    response_model=EnterpriseHistoryAdminDetailRead,
    summary="Удалить главное изображение детального блока",
)
async def delete_enterprise_history_detail_main_image(
    item_id: int,
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.delete_detail_main_image(item_id)


@router.post(
    "/{item_id}/how-it-was",
    response_model=EnterpriseHistoryAdminDetailRead,
    summary="Добавить слайд в блок Как это было",
)
async def add_enterprise_history_slide(
    item_id: int,
    text: str | None = Form(None),
    order_index: int | None = Form(None, ge=0),
    image: UploadFile | None = File(None),
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.add_how_it_was_slide(
        item_id,
        text=text,
        image=image,
        order_index=order_index,
    )


@router.patch(
    "/{item_id}/how-it-was/{slide_id}",
    response_model=EnterpriseHistoryAdminDetailRead,
    summary="Обновить слайд блока Как это было",
)
async def update_enterprise_history_slide(
    item_id: int,
    slide_id: int,
    data: EnterpriseHistorySlideUpdate,
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    if not data.model_fields_set:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Для обновления нужно передать хотя бы одно поле",
        )
    return await service.update_how_it_was_slide(
        item_id,
        slide_id,
        text_provided="text" in data.model_fields_set,
        text=data.text,
        order_index=data.order_index,
    )


@router.put(
    "/{item_id}/how-it-was/{slide_id}/image",
    response_model=EnterpriseHistoryAdminDetailRead,
    summary="Загрузить или заменить изображение слайда",
)
async def update_enterprise_history_slide_image(
    item_id: int,
    slide_id: int,
    image: UploadFile = File(...),
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.update_how_it_was_slide_image(item_id, slide_id, image)


@router.delete(
    "/{item_id}/how-it-was/{slide_id}/image",
    response_model=EnterpriseHistoryAdminDetailRead,
    summary="Удалить изображение слайда",
)
async def delete_enterprise_history_slide_image(
    item_id: int,
    slide_id: int,
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.delete_how_it_was_slide_image(item_id, slide_id)


@router.delete(
    "/{item_id}/how-it-was/{slide_id}",
    response_model=EnterpriseHistoryAdminDetailRead,
    summary="Удалить слайд блока Как это было",
)
async def delete_enterprise_history_slide(
    item_id: int,
    slide_id: int,
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.delete_how_it_was_slide(item_id, slide_id)


@router.put(
    "/{item_id}/how-it-was/order",
    response_model=EnterpriseHistoryAdminDetailRead,
    summary="Изменить порядок слайдов блока Как это было",
)
async def reorder_enterprise_history_slides(
    item_id: int,
    data: EnterpriseHistorySlideOrderUpdate,
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.reorder_how_it_was_slides(item_id, data.slide_ids)


@router.post(
    "/{item_id}/gallery",
    response_model=EnterpriseHistoryAdminDetailRead,
    summary="Добавить изображения в галерею истории предприятия",
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
                                "items": {"type": "string", "format": "binary"},
                            }
                        },
                    }
                }
            },
        }
    },
)
async def add_enterprise_history_gallery_images(
    item_id: int,
    images: list[UploadFile] = File(...),
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.add_gallery_images(item_id, images)


@router.delete(
    "/{item_id}/gallery/{image_id}",
    response_model=EnterpriseHistoryAdminDetailRead,
    summary="Удалить изображение из галереи истории предприятия",
)
async def delete_enterprise_history_gallery_image(
    item_id: int,
    image_id: int,
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.delete_gallery_image(item_id, image_id)


@router.put(
    "/{item_id}/gallery/order",
    response_model=EnterpriseHistoryAdminDetailRead,
    summary="Изменить порядок изображений в галерее истории предприятия",
)
async def reorder_enterprise_history_gallery(
    item_id: int,
    data: EnterpriseHistoryGalleryOrderUpdate,
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.reorder_gallery(item_id, data.image_ids)


@router.delete(
    "/{item_id}",
    summary="Удалить историю предприятия",
)
async def delete_enterprise_history(
    item_id: int,
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    await service.delete_item(item_id)
    return {"detail": "История предприятия удалена"}
