from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class StudentProject(Base):
    __tablename__ = "student_projects"
    __table_args__ = (
        CheckConstraint(
            "year IS NULL OR year >= 1",
            name="ck_student_projects_year_positive",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    author: Mapped[str | None] = mapped_column(String(255), nullable=True)
    short_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    main_image: Mapped[str | None] = mapped_column(String(500), nullable=True)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    tag_one: Mapped[str | None] = mapped_column(String(100), nullable=True)
    tag_two: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_draft: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    gallery_images: Mapped[list["StudentProjectGalleryImage"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
        order_by="StudentProjectGalleryImage.position",
    )


class StudentProjectGalleryImage(Base):
    __tablename__ = "student_project_gallery_images"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("student_projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    image: Mapped[str] = mapped_column(String(500), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    project: Mapped[StudentProject] = relationship(back_populates="gallery_images")
