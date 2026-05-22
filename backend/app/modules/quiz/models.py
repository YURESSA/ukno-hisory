from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Integer, String, Text
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
