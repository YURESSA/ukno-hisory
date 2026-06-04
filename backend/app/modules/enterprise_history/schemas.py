from pydantic import BaseModel, ConfigDict, Field


class EnterpriseHistorySummaryRead(BaseModel):
    id: int
    title: str
    subdistrict: str
    subtitle: str
    short_description: str
    main_image: str

    model_config = ConfigDict(from_attributes=True)


class EnterpriseHistorySlideRead(BaseModel):
    id: int
    text: str | None
    image: str | None
    order_index: int

    model_config = ConfigDict(from_attributes=True)


class EnterpriseHistoryGalleryImageRead(BaseModel):
    id: int
    image: str
    position: int

    model_config = ConfigDict(from_attributes=True)


class EnterpriseHistoryDetailRead(BaseModel):
    id: int
    title: str
    subdistrict: str
    subtitle: str
    short_description: str
    main_image: str
    how_it_was: list[EnterpriseHistorySlideRead]
    gallery: list[EnterpriseHistoryGalleryImageRead]


class EnterpriseHistoryAdminSummaryRead(BaseModel):
    id: int
    title: str | None
    subdistrict: str | None
    general_subtitle: str | None
    short_description: str | None
    general_main_image: str | None
    is_draft: bool

    model_config = ConfigDict(from_attributes=True)


class EnterpriseHistoryAdminDetailRead(BaseModel):
    id: int
    title: str | None
    subdistrict: str | None
    general_subtitle: str | None
    detail_subtitle: str | None
    short_description: str | None
    general_main_image: str | None
    detail_main_image: str | None
    is_draft: bool
    how_it_was: list[EnterpriseHistorySlideRead]
    gallery: list[EnterpriseHistoryGalleryImageRead]


class EnterpriseHistoryUpdate(BaseModel):
    title: str | None = None
    subdistrict: str | None = None
    general_subtitle: str | None = None
    detail_subtitle: str | None = None
    short_description: str | None = None
    is_draft: bool | None = None


class EnterpriseHistorySlideUpdate(BaseModel):
    text: str | None = None
    order_index: int | None = Field(default=None, ge=0)


class EnterpriseHistorySlideOrderUpdate(BaseModel):
    slide_ids: list[int]


class EnterpriseHistoryGalleryOrderUpdate(BaseModel):
    image_ids: list[int]
