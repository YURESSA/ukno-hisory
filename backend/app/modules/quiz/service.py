from datetime import UTC, datetime

from fastapi import HTTPException, status

from app.modules.quiz.files import QuizFileStorage
from app.modules.quiz.models import (
    QuizAttempt,
    QuizAttemptAnswer,
    QuizQuestion,
    QuizQuestionOption,
)
from app.modules.quiz.schemas import (
    QuizAdminStatsRead,
    QuizAnswerSubmit,
    QuizQuestionCreate,
    QuizQuestionDropoffStatsRead,
    QuizQuestionOptionStatsRead,
    QuizQuestionRead,
    QuizQuestionStatsRead,
    QuizQuestionUpdate,
    QuizSubmitRequest,
    QuizSubmitResultRead,
    QuizSubmittedAnswerRead,
)


class QuizService:
    def __init__(self, repo, file_storage: QuizFileStorage):
        self.repo = repo
        self.file_storage = file_storage

    async def create_question(self, data: QuizQuestionCreate, image=None):
        question_text = self._clean_required_text(data.question, "question")
        explanation = self._clean_optional_text(data.explanation)
        normalized_options = self._normalize_options(data.options)
        image_path = None
        if image is not None:
            image_path = await self.file_storage.save_image(image)

        item = QuizQuestion(
            question=question_text,
            explanation=explanation,
            image=image_path,
            options=[
                QuizQuestionOption(
                    text=option["text"],
                    is_correct=option["is_correct"],
                    position=index,
                )
                for index, option in enumerate(normalized_options)
            ],
        )
        created = await self.repo.create(item)
        return self._build_read(created)

    async def get_questions(self):
        items = await self.repo.get_all()
        return [self._build_read(item) for item in items]

    async def get_question(self, item_id: int):
        item = await self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Вопрос квиза не найден",
            )
        return self._build_read(item)

    async def submit_quiz(self, data: QuizSubmitRequest):
        questions = await self.repo.get_all()
        if not questions:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Нельзя отправить результаты пустого квиза",
            )

        answers_by_question_id: dict[int, QuizAnswerSubmit] = {}
        for answer in data.answers:
            if answer.question_id in answers_by_question_id:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail="Ответ на каждый вопрос можно передать только один раз",
                )
            answers_by_question_id[answer.question_id] = answer

        valid_question_ids = {question.id for question in questions}
        unknown_question_ids = sorted(
            question_id
            for question_id in answers_by_question_id
            if question_id not in valid_question_ids
        )
        if unknown_question_ids:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=(
                    "Переданы ответы на несуществующие вопросы: "
                    + ", ".join(str(item) for item in unknown_question_ids)
                ),
            )

        submitted_answers: list[QuizAttemptAnswer] = []
        result_answers: list[QuizSubmittedAnswerRead] = []
        correct_count = 0
        incorrect_count = 0
        unanswered_count = 0

        for question in questions:
            submitted = answers_by_question_id.get(question.id)
            selected_option = None
            is_correct = False

            if submitted is None or submitted.selected_option_id is None:
                unanswered_count += 1
            else:
                selected_option = next(
                    (
                        option
                        for option in question.options
                        if option.id == submitted.selected_option_id
                    ),
                    None,
                )
                if selected_option is None:
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                        detail=(
                            f"Вопрос {question.id} не содержит вариант ответа "
                            f"{submitted.selected_option_id}"
                        ),
                    )
                is_correct = selected_option.is_correct
                if is_correct:
                    correct_count += 1
                else:
                    incorrect_count += 1

            submitted_answers.append(
                QuizAttemptAnswer(
                    question_id=question.id,
                    selected_option_id=selected_option.id if selected_option else None,
                    is_correct=is_correct,
                )
            )
            result_answers.append(
                QuizSubmittedAnswerRead(
                    question_id=question.id,
                    selected_option_id=selected_option.id if selected_option else None,
                    is_correct=is_correct,
                )
            )

        total_questions = len(questions)
        answered_questions = total_questions - unanswered_count
        score_percent = (
            round((correct_count / total_questions) * 100) if total_questions else 0
        )
        completed_at = self._utcnow() if data.is_completed else None

        attempt = QuizAttempt(
            is_completed=data.is_completed,
            completed_at=completed_at,
            total_questions=total_questions,
            answered_questions=answered_questions,
            correct_answers_count=correct_count,
            incorrect_answers_count=incorrect_count,
            unanswered_questions_count=unanswered_count,
            score_percent=score_percent,
            answers=submitted_answers,
        )
        created = await self.repo.create_attempt(attempt)

        return QuizSubmitResultRead(
            attempt_id=created.id,
            is_completed=created.is_completed,
            started_at=created.created_at.isoformat(),
            completed_at=(
                created.completed_at.isoformat() if created.completed_at else None
            ),
            duration_seconds=self._duration_seconds(created),
            total_questions=created.total_questions,
            answered_questions=created.answered_questions,
            correct_answers_count=created.correct_answers_count,
            incorrect_answers_count=created.incorrect_answers_count,
            unanswered_questions_count=created.unanswered_questions_count,
            score_percent=created.score_percent,
            answers=result_answers,
        )

    async def get_admin_stats(self):
        questions = await self.repo.get_all()
        attempts = await self.repo.get_all_attempts()
        total_attempts = len(attempts)
        completed_attempts_count = sum(
            1 for attempt in attempts if attempt.is_completed
        )
        completion_rate_percent = (
            round((completed_attempts_count / total_attempts) * 100)
            if total_attempts
            else 0
        )
        question_order_dropoff = self._build_question_dropoff_stats(questions, attempts)

        question_stats: list[QuizQuestionStatsRead] = []
        for question in questions:
            answers = [
                answer
                for attempt in attempts
                for answer in attempt.answers
                if answer.question_id == question.id
            ]
            answered = [
                answer for answer in answers if answer.selected_option_id is not None
            ]
            total_question_answers = len(answered)
            correct_question_answers = sum(
                1 for answer in answered if answer.is_correct
            )
            incorrect_question_answers = (
                total_question_answers - correct_question_answers
            )
            skipped_count = total_attempts - total_question_answers
            correct_rate_percent = (
                round((correct_question_answers / total_question_answers) * 100)
                if total_question_answers
                else 0
            )

            option_stats: list[QuizQuestionOptionStatsRead] = []
            for option in question.options:
                option_answers_count = sum(
                    1 for answer in answered if answer.selected_option_id == option.id
                )
                share_percent = (
                    round((option_answers_count / total_question_answers) * 100)
                    if total_question_answers
                    else 0
                )
                option_stats.append(
                    QuizQuestionOptionStatsRead(
                        option_id=option.id,
                        text=option.text,
                        answers_count=option_answers_count,
                        share_percent=share_percent,
                        is_correct=option.is_correct,
                    )
                )

            question_stats.append(
                QuizQuestionStatsRead(
                    question_id=question.id,
                    question=question.question,
                    total_answers=total_question_answers,
                    correct_answers_count=correct_question_answers,
                    incorrect_answers_count=incorrect_question_answers,
                    skipped_count=skipped_count,
                    correct_rate_percent=correct_rate_percent,
                    option_stats=option_stats,
                )
            )

        return QuizAdminStatsRead(
            completion_rate_percent=completion_rate_percent,
            question_order_dropoff=question_order_dropoff,
            questions=question_stats,
        )

    async def update_question(self, item_id: int, data: QuizQuestionUpdate):
        item = await self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Вопрос квиза не найден",
            )

        if "question" in data.model_fields_set:
            item.question = self._clean_required_text(data.question, "question")
        if "explanation" in data.model_fields_set:
            item.explanation = self._clean_optional_text(data.explanation)
        if "options" in data.model_fields_set:
            normalized_options = self._normalize_options(data.options or [])
            item.options.clear()
            item.options.extend(
                QuizQuestionOption(
                    text=option["text"],
                    is_correct=option["is_correct"],
                    position=index,
                )
                for index, option in enumerate(normalized_options)
            )

        await self.repo.session.commit()
        item = await self.repo.get_by_id(item.id)
        return self._build_read(item)

    async def update_question_image(self, item_id: int, image):
        item = await self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Вопрос квиза не найден",
            )

        old_image = item.image
        item.image = await self.file_storage.save_image(image)
        await self.repo.session.commit()
        item = await self.repo.get_by_id(item.id)

        if old_image is not None:
            self.file_storage.delete_image(old_image)

        return self._build_read(item)

    async def delete_question_image(self, item_id: int):
        item = await self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Вопрос квиза не найден",
            )

        image_path = item.image
        item.image = None
        await self.repo.session.commit()
        item = await self.repo.get_by_id(item.id)

        if image_path is not None:
            self.file_storage.delete_image(image_path)

        return self._build_read(item)

    async def delete_question(self, item_id: int):
        item = await self.repo.get_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Вопрос квиза не найден",
            )

        image_path = item.image
        await self.repo.delete(item)
        if image_path is not None:
            self.file_storage.delete_image(image_path)

    def _normalize_options(self, options) -> list[dict[str, str | bool]]:
        if len(options) < 2:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="У вопроса должно быть минимум два варианта ответа",
            )

        normalized_options: list[dict[str, str | bool]] = []
        correct_count = 0
        for option in options:
            text = self._clean_required_text(option.text, "option")
            is_correct = option.is_correct
            if is_correct:
                correct_count += 1
            normalized_options.append({"text": text, "is_correct": is_correct})

        if correct_count != 1:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="У вопроса должен быть ровно один правильный ответ",
            )

        return normalized_options

    def _clean_required_text(self, value: str | None, field_name: str) -> str:
        cleaned = self._clean_optional_text(value)
        if cleaned is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f"Поле {field_name} не может быть пустым",
            )
        return cleaned

    def _clean_optional_text(self, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        return cleaned or None

    def _utcnow(self) -> datetime:
        return datetime.now(UTC)

    def _duration_seconds(self, attempt: QuizAttempt) -> int | None:
        if attempt.completed_at is None:
            return None
        return max(
            0, round((attempt.completed_at - attempt.created_at).total_seconds())
        )

    def _build_question_dropoff_stats(
        self,
        questions: list[QuizQuestion],
        attempts: list[QuizAttempt],
    ) -> list[QuizQuestionDropoffStatsRead]:
        if not questions or not attempts:
            return []

        dropoff_counts = {question.id: 0 for question in questions}
        for attempt in attempts:
            answers_by_question_id = {
                answer.question_id: answer for answer in attempt.answers
            }
            for _index, question in enumerate(questions):
                answer = answers_by_question_id.get(question.id)
                if answer is None or answer.selected_option_id is None:
                    dropoff_counts[question.id] += 1
                    break

        return [
            QuizQuestionDropoffStatsRead(
                question_id=question.id,
                question=question.question,
                order_index=index,
                dropoff_count=dropoff_counts[question.id],
                dropoff_percent=round(
                    (dropoff_counts[question.id] / len(attempts)) * 100
                ),
            )
            for index, question in enumerate(questions)
            if dropoff_counts[question.id] > 0
        ]

    def _build_read(self, item: QuizQuestion) -> QuizQuestionRead:
        return QuizQuestionRead(
            id=item.id,
            question=item.question,
            explanation=item.explanation,
            image=item.image,
            options=item.options,
        )
