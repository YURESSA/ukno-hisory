from pydantic import BaseModel, ConfigDict, Field


class TimelineBase(BaseModel):
    year: int = Field(..., ge=1, description="Год события")
    image: str = Field(..., max_length=500, description="Путь к изображению")
    text: str = Field(..., min_length=1, description="Описание события")


class TimelineCreate(TimelineBase):
    pass


class TimelineUpdate(BaseModel):
    year: int | None = Field(default=None, ge=1, description="Год события")
    text: str | None = Field(default=None, min_length=1, description="Описание события")


class TimelineRead(TimelineBase):
    id: int = Field(..., description="Идентификатор записи")

    model_config = ConfigDict(from_attributes=True)
