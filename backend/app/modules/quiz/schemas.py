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


class QuizAnswerSubmit(BaseModel):
    question_id: int
    selected_option_id: int | None = None


class QuizSubmitRequest(BaseModel):
    is_completed: bool = True
    answers: list[QuizAnswerSubmit]


class QuizSubmittedAnswerRead(BaseModel):
    question_id: int
    selected_option_id: int | None
    is_correct: bool


class QuizSubmitResultRead(BaseModel):
    attempt_id: int
    is_completed: bool
    started_at: str
    completed_at: str | None
    duration_seconds: int | None
    total_questions: int
    answered_questions: int
    correct_answers_count: int
    incorrect_answers_count: int
    unanswered_questions_count: int
    score_percent: int
    answers: list[QuizSubmittedAnswerRead]


class QuizQuestionOptionStatsRead(BaseModel):
    option_id: int
    text: str
    answers_count: int
    share_percent: int
    is_correct: bool


class QuizQuestionStatsRead(BaseModel):
    question_id: int
    question: str
    total_answers: int
    correct_answers_count: int
    incorrect_answers_count: int
    skipped_count: int
    correct_rate_percent: int
    option_stats: list[QuizQuestionOptionStatsRead]


class QuizQuestionDropoffStatsRead(BaseModel):
    question_id: int
    question: str
    order_index: int
    dropoff_count: int
    dropoff_percent: int


class QuizAdminStatsRead(BaseModel):
    completion_rate_percent: int
    question_order_dropoff: list[QuizQuestionDropoffStatsRead]
    questions: list[QuizQuestionStatsRead]
