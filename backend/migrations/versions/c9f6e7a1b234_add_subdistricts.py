"""add subdistricts

Revision ID: c9f6e7a1b234
Revises: a7d4d7f5c642
Create Date: 2026-06-04 10:55:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "c9f6e7a1b234"
down_revision = "a7d4d7f5c642"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "enterprise_histories",
        sa.Column("subdistrict", sa.String(length=100), nullable=True),
    )
    op.create_index(
        op.f("ix_enterprise_histories_subdistrict"),
        "enterprise_histories",
        ["subdistrict"],
        unique=False,
    )

    op.create_table(
        "subdistrict_contents",
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("image", sa.String(length=500), nullable=True),
        sa.PrimaryKeyConstraint("name"),
    )


def downgrade() -> None:
    op.drop_table("subdistrict_contents")
    op.drop_index(
        op.f("ix_enterprise_histories_subdistrict"),
        table_name="enterprise_histories",
    )
    op.drop_column("enterprise_histories", "subdistrict")
