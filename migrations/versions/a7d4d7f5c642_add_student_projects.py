"""add student projects

Revision ID: a7d4d7f5c642
Revises: 785fba5a0a11
Create Date: 2026-04-26 16:20:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a7d4d7f5c642"
down_revision: Union[str, Sequence[str], None] = "785fba5a0a11"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "student_projects",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=True),
        sa.Column("author", sa.String(length=255), nullable=True),
        sa.Column("short_description", sa.Text(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("main_image", sa.String(length=500), nullable=True),
        sa.Column("year", sa.Integer(), nullable=True),
        sa.Column("tag_one", sa.String(length=100), nullable=True),
        sa.Column("tag_two", sa.String(length=100), nullable=True),
        sa.Column("is_draft", sa.Boolean(), nullable=False),
        sa.CheckConstraint(
            "year IS NULL OR year >= 1",
            name="ck_student_projects_year_positive",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_student_projects_id"),
        "student_projects",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_student_projects_title"),
        "student_projects",
        ["title"],
        unique=False,
    )
    op.create_index(
        op.f("ix_student_projects_year"),
        "student_projects",
        ["year"],
        unique=False,
    )
    op.create_table(
        "student_project_gallery_images",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("image", sa.String(length=500), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["student_projects.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_student_project_gallery_images_id"),
        "student_project_gallery_images",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_student_project_gallery_images_project_id"),
        "student_project_gallery_images",
        ["project_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        op.f("ix_student_project_gallery_images_project_id"),
        table_name="student_project_gallery_images",
    )
    op.drop_index(
        op.f("ix_student_project_gallery_images_id"),
        table_name="student_project_gallery_images",
    )
    op.drop_table("student_project_gallery_images")
    op.drop_index(op.f("ix_student_projects_year"), table_name="student_projects")
    op.drop_index(op.f("ix_student_projects_title"), table_name="student_projects")
    op.drop_index(op.f("ix_student_projects_id"), table_name="student_projects")
    op.drop_table("student_projects")
