"""add quiz questions

Revision ID: 5e0a3c7c9c11
Revises: e065717df88d
Create Date: 2026-05-22 12:45:00.000000

"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5e0a3c7c9c11"
down_revision: str | None = "4c1f9f0c2a11"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "quiz_questions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=True),
        sa.Column("image", sa.String(length=500), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_quiz_questions_id"), "quiz_questions", ["id"], unique=False
    )

    op.create_table(
        "quiz_question_options",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("is_correct", sa.Boolean(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.CheckConstraint(
            "position >= 0",
            name="ck_quiz_question_options_position_non_negative",
        ),
        sa.ForeignKeyConstraint(
            ["question_id"],
            ["quiz_questions.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_quiz_question_options_id"),
        "quiz_question_options",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_quiz_question_options_question_id"),
        "quiz_question_options",
        ["question_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_quiz_question_options_question_id"),
        table_name="quiz_question_options",
    )
    op.drop_index(
        op.f("ix_quiz_question_options_id"),
        table_name="quiz_question_options",
    )
    op.drop_table("quiz_question_options")
    op.drop_index(op.f("ix_quiz_questions_id"), table_name="quiz_questions")
    op.drop_table("quiz_questions")
