"""fix timeline year constraint

Revision ID: 785fba5a0a11
Revises: e065717df88d
Create Date: 2026-04-26 15:55:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "785fba5a0a11"
down_revision: Union[str, Sequence[str], None] = "e065717df88d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("UPDATE timeline_entries SET year = 1 WHERE year < 1")

    with op.batch_alter_table("timeline_entries", recreate="always") as batch_op:
        batch_op.create_check_constraint(
            "ck_timeline_entries_year_positive",
            condition=sa.text("year >= 1"),
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("timeline_entries", recreate="always") as batch_op:
        batch_op.drop_constraint(
            "ck_timeline_entries_year_positive",
            type_="check",
        )
