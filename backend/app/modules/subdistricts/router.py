from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.core.database import get_db
from app.core.dependencies import require_admin
from app.modules.subdistricts.files import SubdistrictFileStorage
from app.modules.subdistricts.repository import SubdistrictRepository
from app.modules.subdistricts.schemas import (
    SubdistrictAdminUpdate,
    SubdistrictDetailRead,
    SubdistrictRead,
)
from app.modules.subdistricts.service import SubdistrictService

router = APIRouter()


def get_service(db=Depends(get_db)):
    return SubdistrictService(
        SubdistrictRepository(db),
        SubdistrictFileStorage(),
    )


@router.get(
    "",
    response_model=list[SubdistrictRead],
    summary="Получить список подрайонов",
)
async def get_subdistricts(service=Depends(get_service)):
    return await service.get_all()


@router.get(
    "/{subdistrict_name}",
    response_model=SubdistrictDetailRead,
    summary="Получить данные подрайона для интерактивной карты",
)
async def get_subdistrict_detail(subdistrict_name: str, service=Depends(get_service)):
    return await service.get_detail(subdistrict_name)


@router.patch(
    "/{subdistrict_name}",
    response_model=SubdistrictDetailRead,
    summary="Обновить описание подрайона",
)
async def update_subdistrict(
    subdistrict_name: str,
    data: SubdistrictAdminUpdate,
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    if not data.model_fields_set:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Для обновления нужно передать хотя бы одно поле",
        )

    return await service.update_content(
        subdistrict_name,
        description=data.description,
    )


@router.put(
    "/{subdistrict_name}/image",
    response_model=SubdistrictDetailRead,
    summary="Загрузить или заменить изображение подрайона",
)
async def update_subdistrict_image(
    subdistrict_name: str,
    image: UploadFile = File(...),
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.update_image(subdistrict_name, image)


@router.delete(
    "/{subdistrict_name}/image",
    response_model=SubdistrictDetailRead,
    summary="Удалить изображение подрайона",
)
async def delete_subdistrict_image(
    subdistrict_name: str,
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.delete_image(subdistrict_name)
