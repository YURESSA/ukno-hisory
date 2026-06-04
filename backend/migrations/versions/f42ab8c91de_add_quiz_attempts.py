"""add quiz attempts

Revision ID: f42ab8c91de
Revises: b1b7c9d2e3f4
Create Date: 2026-06-04 12:20:00.000000
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "f42ab8c91de"
down_revision: str | None = "b1b7c9d2e3f4"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "quiz_attempts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("total_questions", sa.Integer(), nullable=False),
        sa.Column("answered_questions", sa.Integer(), nullable=False),
        sa.Column("correct_answers_count", sa.Integer(), nullable=False),
        sa.Column("incorrect_answers_count", sa.Integer(), nullable=False),
        sa.Column("unanswered_questions_count", sa.Integer(), nullable=False),
        sa.Column("score_percent", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "correct_answers_count >= 0",
            name="ck_quiz_attempts_correct_answers_count_non_negative",
        ),
        sa.CheckConstraint(
            "incorrect_answers_count >= 0",
            name="ck_quiz_attempts_incorrect_answers_count_non_negative",
        ),
        sa.CheckConstraint(
            "unanswered_questions_count >= 0",
            name="ck_quiz_attempts_unanswered_questions_count_non_negative",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_quiz_attempts_id"), "quiz_attempts", ["id"], unique=False)

    op.create_table(
        "quiz_attempt_answers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("attempt_id", sa.Integer(), nullable=False),
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("selected_option_id", sa.Integer(), nullable=True),
        sa.Column("is_correct", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["attempt_id"], ["quiz_attempts.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["question_id"], ["quiz_questions.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["selected_option_id"],
            ["quiz_question_options.id"],
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_quiz_attempt_answers_id"),
        "quiz_attempt_answers",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_quiz_attempt_answers_attempt_id"),
        "quiz_attempt_answers",
        ["attempt_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_quiz_attempt_answers_question_id"),
        "quiz_attempt_answers",
        ["question_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_quiz_attempt_answers_selected_option_id"),
        "quiz_attempt_answers",
        ["selected_option_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_quiz_attempt_answers_selected_option_id"),
        table_name="quiz_attempt_answers",
    )
    op.drop_index(
        op.f("ix_quiz_attempt_answers_question_id"),
        table_name="quiz_attempt_answers",
    )
    op.drop_index(
        op.f("ix_quiz_attempt_answers_attempt_id"),
        table_name="quiz_attempt_answers",
    )
    op.drop_index(op.f("ix_quiz_attempt_answers_id"), table_name="quiz_attempt_answers")
    op.drop_table("quiz_attempt_answers")
    op.drop_index(op.f("ix_quiz_attempts_id"), table_name="quiz_attempts")
    op.drop_table("quiz_attempts")
