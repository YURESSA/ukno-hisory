from pydantic import BaseModel, ConfigDict, Field


class StudentProjectSummaryRead(BaseModel):
    id: int
    title: str
    author: str
    short_description: str
    main_image: str

    model_config = ConfigDict(from_attributes=True)


class StudentProjectTagRead(BaseModel):
    author: str
    year: int
    tag_one: str | None
    tag_two: str | None


class StudentProjectGalleryImageRead(BaseModel):
    id: int
    image: str
    position: int

    model_config = ConfigDict(from_attributes=True)


class StudentProjectDetailRead(BaseModel):
    id: int
    title: str
    main_image: str
    description: str
    tags: StudentProjectTagRead
    gallery: list[StudentProjectGalleryImageRead]


class StudentProjectAdminSummaryRead(BaseModel):
    id: int
    title: str | None
    author: str | None
    short_description: str | None
    main_image: str | None
    is_draft: bool

    model_config = ConfigDict(from_attributes=True)


class StudentProjectAdminDetailRead(BaseModel):
    id: int
    title: str | None
    author: str | None
    short_description: str | None
    description: str | None
    main_image: str | None
    year: int | None
    tag_one: str | None
    tag_two: str | None
    is_draft: bool
    gallery: list[StudentProjectGalleryImageRead]

    model_config = ConfigDict(from_attributes=True)


class StudentProjectUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    short_description: str | None = None
    description: str | None = None
    year: int | None = Field(default=None, ge=1)
    tag_one: str | None = None
    tag_two: str | None = None
    is_draft: bool | None = None


class StudentProjectGalleryOrderUpdate(BaseModel):
    image_ids: list[int]
