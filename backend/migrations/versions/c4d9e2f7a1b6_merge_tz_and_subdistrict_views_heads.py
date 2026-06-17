"""merge tz and subdistrict views heads

Revision ID: c4d9e2f7a1b6
Revises: b6d4f2a1c9e8, f8b3c1a7d942
Create Date: 2026-06-11 17:05:00.000000
"""

from collections.abc import Sequence

revision: str = "c4d9e2f7a1b6"
down_revision: Sequence[str] | None = ("b6d4f2a1c9e8", "f8b3c1a7d942")
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
