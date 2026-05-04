from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from app.core.database import get_db
from app.core.dependencies import require_admin
from app.modules.timeline.files import TimelineFileStorage
from app.modules.timeline.repository import TimelineRepository
from app.modules.timeline.schemas import TimelineRead, TimelineUpdate
from app.modules.timeline.service import TimelineService

router = APIRouter()


def get_service(db=Depends(get_db)):
    return TimelineService(TimelineRepository(db), TimelineFileStorage())


@router.get(
    "",
    response_model=list[TimelineRead],
    status_code=status.HTTP_200_OK,
    summary="Получить список записей таймлайна",
)
async def get_timeline_entries(service=Depends(get_service)):
    return await service.get_entries()


@router.get(
    "/{entry_id}",
    response_model=TimelineRead,
    status_code=status.HTTP_200_OK,
    summary="Получить запись таймлайна по идентификатору",
)
async def get_timeline_entry(entry_id: int, service=Depends(get_service)):
    return await service.get_entry(entry_id)


@router.post(
    "",
    response_model=TimelineRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать запись таймлайна",
)
async def create_timeline_entry(
    year: int = Form(..., ge=1),
    text: str = Form(..., min_length=1),
    image: UploadFile = File(...),
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.create_entry(year, image, text)


@router.patch(
    "/{entry_id}",
    response_model=TimelineRead,
    status_code=status.HTTP_200_OK,
    summary="Обновить данные записи таймлайна",
)
async def update_timeline_entry(
    entry_id: int,
    data: TimelineUpdate,
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    if not data.model_fields_set:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Для обновления нужно передать хотя бы одно поле",
        )

    return await service.update_entry(entry_id, data)


@router.put(
    "/{entry_id}/image",
    response_model=TimelineRead,
    status_code=status.HTTP_200_OK,
    summary="Загрузить или заменить изображение записи таймлайна",
)
async def update_timeline_entry_image(
    entry_id: int,
    image: UploadFile = File(...),
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.update_entry_image(entry_id, image)


@router.delete(
    "/{entry_id}/image",
    response_model=TimelineRead,
    status_code=status.HTTP_200_OK,
    summary="Удалить изображение записи таймлайна",
)
async def delete_timeline_entry_image(
    entry_id: int,
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.delete_entry_image(entry_id)


@router.delete(
    "/{entry_id}",
    status_code=status.HTTP_200_OK,
    summary="Удалить запись таймлайна",
)
async def delete_timeline_entry(
    entry_id: int,
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    await service.delete_entry(entry_id)
    return {"detail": "Запись таймлайна удалена"}
