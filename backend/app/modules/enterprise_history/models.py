from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class EnterpriseHistory(Base):
    __tablename__ = "enterprise_histories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    subdistrict: Mapped[str | None] = mapped_column(
        String(100), nullable=True, index=True
    )
    general_subtitle: Mapped[str | None] = mapped_column(String(255), nullable=True)
    detail_subtitle: Mapped[str | None] = mapped_column(String(255), nullable=True)
    short_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    general_main_image: Mapped[str | None] = mapped_column(String(500), nullable=True)
    detail_main_image: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_draft: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    how_it_was_slides: Mapped[list["EnterpriseHistorySlide"]] = relationship(
        back_populates="enterprise_history",
        cascade="all, delete-orphan",
        order_by="EnterpriseHistorySlide.order_index",
    )
    gallery_images: Mapped[list["EnterpriseHistoryGalleryImage"]] = relationship(
        back_populates="enterprise_history",
        cascade="all, delete-orphan",
        order_by="EnterpriseHistoryGalleryImage.position",
    )


class EnterpriseHistorySlide(Base):
    __tablename__ = "enterprise_history_slides"
    __table_args__ = (
        CheckConstraint(
            "order_index >= 0",
            name="ck_enterprise_history_slides_order_index_non_negative",
        ),
        CheckConstraint(
            "text IS NOT NULL OR image IS NOT NULL",
            name="ck_enterprise_history_slides_has_content",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    enterprise_history_id: Mapped[int] = mapped_column(
        ForeignKey("enterprise_histories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    text: Mapped[str | None] = mapped_column(Text, nullable=True)
    image: Mapped[str | None] = mapped_column(String(500), nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    enterprise_history: Mapped[EnterpriseHistory] = relationship(
        back_populates="how_it_was_slides"
    )


class EnterpriseHistoryGalleryImage(Base):
    __tablename__ = "enterprise_history_gallery_images"
    __table_args__ = (
        CheckConstraint(
            "position >= 0",
            name="ck_enterprise_history_gallery_images_position_non_negative",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    enterprise_history_id: Mapped[int] = mapped_column(
        ForeignKey("enterprise_histories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    image: Mapped[str] = mapped_column(String(500), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    enterprise_history: Mapped[EnterpriseHistory] = relationship(
        back_populates="gallery_images"
    )
