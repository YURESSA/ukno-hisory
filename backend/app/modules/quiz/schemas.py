from pydantic import BaseModel, ConfigDict, Field

QUIZ_OPTIONS_EXAMPLE = [
    {"text": "Париж", "is_correct": False},
    {"text": "Москва", "is_correct": True},
    {"text": "Берлин", "is_correct": False},
]


class QuizOptionBase(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        description="Текст варианта ответа",
        examples=["Москва"],
    )
    is_correct: bool = Field(
        ...,
        description="Признак правильного ответа",
        examples=[True],
    )


class QuizOptionCreate(QuizOptionBase):
    pass


class QuizOptionRead(QuizOptionBase):
    id: int
    position: int

    model_config = ConfigDict(from_attributes=True)


class QuizQuestionCreate(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="Текст вопроса",
        examples=["Столица России?"],
    )
    explanation: str | None = Field(
        default=None,
        description="Пояснение к правильному ответу",
        examples=["Москва является столицей России."],
    )
    options: list[QuizOptionCreate] = Field(
        ...,
        min_length=2,
        description=(
            "Список вариантов ответа. Формат: "
            '[{"text":"Вариант 1","is_correct":false},'
            '{"text":"Вариант 2","is_correct":true}]'
        ),
        examples=[QUIZ_OPTIONS_EXAMPLE],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "question": "Столица России?",
                "explanation": "Москва является столицей России.",
                "options": QUIZ_OPTIONS_EXAMPLE,
            }
        }
    )


class QuizQuestionUpdate(BaseModel):
    question: str | None = Field(default=None, min_length=1)
    explanation: str | None = None
    options: list[QuizOptionCreate] | None = Field(
        default=None,
        min_length=2,
        examples=[QUIZ_OPTIONS_EXAMPLE],
    )


class QuizQuestionRead(BaseModel):
    id: int
    question: str
    explanation: str | None
    image: str | None
    options: list[QuizOptionRead]

    model_config = ConfigDict(from_attributes=True)
