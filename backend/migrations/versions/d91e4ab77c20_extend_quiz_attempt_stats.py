"""extend quiz attempt stats

Revision ID: d91e4ab77c20
Revises: f42ab8c91de
Create Date: 2026-06-04 13:10:00.000000
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "d91e4ab77c20"
down_revision: str | None = "f42ab8c91de"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "quiz_attempts",
        sa.Column("completed_at", sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("quiz_attempts", "completed_at")
