"""merge quiz and subdistrict heads

Revision ID: e4f2b2a7c8d1
Revises: c9f6e7a1b234, d91e4ab77c20
Create Date: 2026-06-04 14:45:00.000000
"""

from collections.abc import Sequence


revision: str = "e4f2b2a7c8d1"
down_revision: Sequence[str] | None = ("c9f6e7a1b234", "d91e4ab77c20")
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
