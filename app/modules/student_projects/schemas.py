from pydantic import BaseModel, ConfigDict


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


class StudentProjectGalleryOrderUpdate(BaseModel):
    image_ids: list[int]
