"""add main site transitions

Revision ID: a3c5e7f9b2d4
Revises: e4f2b2a7c8d1
Create Date: 2026-06-11 16:10:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "a3c5e7f9b2d4"
down_revision: str | None = "e4f2b2a7c8d1"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "main_site_transitions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("client_ip", sa.String(length=100), nullable=True),
        sa.Column("user_agent", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_main_site_transitions_id"),
        "main_site_transitions",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_main_site_transitions_created_at"),
        "main_site_transitions",
        ["created_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_main_site_transitions_created_at"),
        table_name="main_site_transitions",
    )
    op.drop_index(
        op.f("ix_main_site_transitions_id"),
        table_name="main_site_transitions",
    )
    op.drop_table("main_site_transitions")
