"""add subdistrict views count

Revision ID: f8b3c1a7d942
Revises: e4f2b2a7c8d1
Create Date: 2026-06-11 16:40:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f8b3c1a7d942"
down_revision: Union[str, None] = "e4f2b2a7c8d1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "subdistrict_contents",
        sa.Column(
            "views_count",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )
    op.alter_column(
        "subdistrict_contents",
        "views_count",
        server_default=None,
    )


def downgrade() -> None:
    op.drop_column("subdistrict_contents", "views_count")
