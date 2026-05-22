"""repair missing users table

Revision ID: b1b7c9d2e3f4
Revises: 5e0a3c7c9c11
Create Date: 2026-05-22 14:40:00.000000

"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b1b7c9d2e3f4"
down_revision: str | None = "5e0a3c7c9c11"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "users" not in inspector.get_table_names():
        op.create_table(
            "users",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("email", sa.String(length=255), nullable=False),
            sa.Column("password_hash", sa.String(), nullable=False),
            sa.Column("role", sa.String(length=20), nullable=False),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
        op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "users" in inspector.get_table_names():
        indexes = {index["name"] for index in inspector.get_indexes("users")}
        if op.f("ix_users_id") in indexes:
            op.drop_index(op.f("ix_users_id"), table_name="users")
        if op.f("ix_users_email") in indexes:
            op.drop_index(op.f("ix_users_email"), table_name="users")
        op.drop_table("users")
