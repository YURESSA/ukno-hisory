"""add timeline entries table

Revision ID: e065717df88d
Revises: 3180d371d724
Create Date: 2026-04-26 15:30:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e065717df88d"
down_revision: Union[str, Sequence[str], None] = "3180d371d724"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "timeline_entries",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("image", sa.String(length=500), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_timeline_entries_id"), "timeline_entries", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_timeline_entries_year"), "timeline_entries", ["year"], unique=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_timeline_entries_year"), table_name="timeline_entries")
    op.drop_index(op.f("ix_timeline_entries_id"), table_name="timeline_entries")
    op.drop_table("timeline_entries")
