from pydantic import BaseModel, ConfigDict, Field


class TimelineBase(BaseModel):
    year: int = Field(..., ge=1, description="Год события")
    image: str = Field(..., min_length=1, max_length=500)
    text: str = Field(..., min_length=1)


class TimelineCreate(TimelineBase):
    pass


class TimelineUpdate(TimelineBase):
    pass


class TimelineRead(TimelineBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
