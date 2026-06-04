from pydantic import BaseModel, ConfigDict


class SubdistrictEnterpriseRead(BaseModel):
    id: int
    title: str


class SubdistrictRead(BaseModel):
    name: str
    description: str | None
    image: str | None


class SubdistrictDetailRead(SubdistrictRead):
    enterprises: list[SubdistrictEnterpriseRead]


class SubdistrictAdminUpdate(BaseModel):
    description: str | None = None

    model_config = ConfigDict(extra="forbid")
