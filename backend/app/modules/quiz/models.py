from datetime import UTC, datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    image: Mapped[str | None] = mapped_column(String(500), nullable=True)

    options: Mapped[list["QuizQuestionOption"]] = relationship(
        back_populates="question_item",
        cascade="all, delete-orphan",
        order_by="QuizQuestionOption.position",
    )
    attempt_answers: Mapped[list["QuizAttemptAnswer"]] = relationship(
        back_populates="question_item"
    )


class QuizQuestionOption(Base):
    __tablename__ = "quiz_question_options"
    __table_args__ = (
        CheckConstraint(
            "position >= 0",
            name="ck_quiz_question_options_position_non_negative",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    question_id: Mapped[int] = mapped_column(
        ForeignKey("quiz_questions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    text: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    question_item: Mapped[QuizQuestion] = relationship(back_populates="options")
    attempt_answers: Mapped[list["QuizAttemptAnswer"]] = relationship(
        back_populates="selected_option"
    )


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    __table_args__ = (
        CheckConstraint(
            "correct_answers_count >= 0",
            name="ck_quiz_attempts_correct_answers_count_non_negative",
        ),
        CheckConstraint(
            "incorrect_answers_count >= 0",
            name="ck_quiz_attempts_incorrect_answers_count_non_negative",
        ),
        CheckConstraint(
            "unanswered_questions_count >= 0",
            name="ck_quiz_attempts_unanswered_questions_count_non_negative",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    total_questions: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    answered_questions: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    correct_answers_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    incorrect_answers_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    unanswered_questions_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    score_percent: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(UTC)
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    answers: Mapped[list["QuizAttemptAnswer"]] = relationship(
        back_populates="attempt",
        cascade="all, delete-orphan",
        order_by="QuizAttemptAnswer.question_id",
    )


class QuizAttemptAnswer(Base):
    __tablename__ = "quiz_attempt_answers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    attempt_id: Mapped[int] = mapped_column(
        ForeignKey("quiz_attempts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    question_id: Mapped[int] = mapped_column(
        ForeignKey("quiz_questions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    selected_option_id: Mapped[int | None] = mapped_column(
        ForeignKey("quiz_question_options.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    attempt: Mapped[QuizAttempt] = relationship(back_populates="answers")
    question_item: Mapped[QuizQuestion] = relationship(back_populates="attempt_answers")
    selected_option: Mapped[QuizQuestionOption | None] = relationship(
        back_populates="attempt_answers"
    )
