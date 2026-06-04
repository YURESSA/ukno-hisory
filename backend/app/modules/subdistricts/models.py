from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class SubdistrictContent(Base):
    __tablename__ = "subdistrict_contents"

    name: Mapped[str] = mapped_column(String(100), primary_key=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    image: Mapped[str | None] = mapped_column(String(500), nullable=True)
