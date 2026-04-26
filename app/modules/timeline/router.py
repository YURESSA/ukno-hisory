from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from app.core.database import get_db
from app.core.dependencies import require_admin
from app.modules.timeline.files import TimelineFileStorage
from app.modules.timeline.repository import TimelineRepository
from app.modules.timeline.schemas import TimelineRead
from app.modules.timeline.service import TimelineService

router = APIRouter()


def get_service(db=Depends(get_db)):
    return TimelineService(TimelineRepository(db), TimelineFileStorage())


@router.get("", response_model=list[TimelineRead], status_code=status.HTTP_200_OK)
async def get_timeline_entries(service=Depends(get_service)):
    return await service.get_entries()


@router.get("/{entry_id}", response_model=TimelineRead, status_code=status.HTTP_200_OK)
async def get_timeline_entry(entry_id: int, service=Depends(get_service)):
    return await service.get_entry(entry_id)


@router.post("", response_model=TimelineRead, status_code=status.HTTP_201_CREATED)
async def create_timeline_entry(
    year: int = Form(..., ge=1),
    text: str = Form(..., min_length=1),
    image: UploadFile = File(...),
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.create_entry(year, image, text)


@router.put("/{entry_id}", response_model=TimelineRead, status_code=status.HTTP_200_OK)
async def update_timeline_entry(
    entry_id: int,
    year: Annotated[int | None, Form(ge=1)] = None,
    text: Annotated[str | None, Form(min_length=1)] = None,
    image: Annotated[UploadFile | None, File()] = None,
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    if year is None and text is None and image is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="At least one field must be provided for update",
        )

    return await service.update_entry(entry_id, year, image, text)


@router.delete("/{entry_id}", status_code=status.HTTP_200_OK)
async def delete_timeline_entry(
    entry_id: int,
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    await service.delete_entry(entry_id)
    return {"detail": "Timeline entry deleted"}
