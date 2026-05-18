"""add enterprise history

Revision ID: 4c1f9f0c2a11
Revises: a7d4d7f5c642
Create Date: 2026-05-18 12:10:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4c1f9f0c2a11"
down_revision: Union[str, Sequence[str], None] = "a7d4d7f5c642"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "enterprise_histories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column("general_subtitle", sa.String(length=255), nullable=True),
        sa.Column("detail_subtitle", sa.String(length=255), nullable=True),
        sa.Column("short_description", sa.Text(), nullable=True),
        sa.Column("general_main_image", sa.String(length=500), nullable=True),
        sa.Column("detail_main_image", sa.String(length=500), nullable=True),
        sa.Column("is_draft", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_enterprise_histories_id"),
        "enterprise_histories",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_enterprise_histories_title"),
        "enterprise_histories",
        ["title"],
        unique=False,
    )

    op.create_table(
        "enterprise_history_slides",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("enterprise_history_id", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=True),
        sa.Column("image", sa.String(length=500), nullable=True),
        sa.Column("order_index", sa.Integer(), nullable=False),
        sa.CheckConstraint(
            "order_index >= 0",
            name="ck_enterprise_history_slides_order_index_non_negative",
        ),
        sa.CheckConstraint(
            "text IS NOT NULL OR image IS NOT NULL",
            name="ck_enterprise_history_slides_has_content",
        ),
        sa.ForeignKeyConstraint(
            ["enterprise_history_id"],
            ["enterprise_histories.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_enterprise_history_slides_id"),
        "enterprise_history_slides",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_enterprise_history_slides_enterprise_history_id"),
        "enterprise_history_slides",
        ["enterprise_history_id"],
        unique=False,
    )

    op.create_table(
        "enterprise_history_gallery_images",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("enterprise_history_id", sa.Integer(), nullable=False),
        sa.Column("image", sa.String(length=500), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.CheckConstraint(
            "position >= 0",
            name="ck_enterprise_history_gallery_images_position_non_negative",
        ),
        sa.ForeignKeyConstraint(
            ["enterprise_history_id"],
            ["enterprise_histories.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_enterprise_history_gallery_images_id"),
        "enterprise_history_gallery_images",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_enterprise_history_gallery_images_enterprise_history_id"),
        "enterprise_history_gallery_images",
        ["enterprise_history_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        op.f("ix_enterprise_history_gallery_images_enterprise_history_id"),
        table_name="enterprise_history_gallery_images",
    )
    op.drop_index(
        op.f("ix_enterprise_history_gallery_images_id"),
        table_name="enterprise_history_gallery_images",
    )
    op.drop_table("enterprise_history_gallery_images")

    op.drop_index(
        op.f("ix_enterprise_history_slides_enterprise_history_id"),
        table_name="enterprise_history_slides",
    )
    op.drop_index(
        op.f("ix_enterprise_history_slides_id"),
        table_name="enterprise_history_slides",
    )
    op.drop_table("enterprise_history_slides")

    op.drop_index(
        op.f("ix_enterprise_histories_title"), table_name="enterprise_histories"
    )
    op.drop_index(op.f("ix_enterprise_histories_id"), table_name="enterprise_histories")
    op.drop_table("enterprise_histories")
