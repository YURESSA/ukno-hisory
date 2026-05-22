from fastapi import HTTPException, status

from app.modules.quiz.files import QuizFileStorage
from app.modules.quiz.models import QuizQuestion, QuizQuestionOption
from app.modules.quiz.schemas import (
    QuizQuestionCreate,
    QuizQuestionRead,
    QuizQuestionUpdate,
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

    def _build_read(self, item: QuizQuestion) -> QuizQuestionRead:
        return QuizQuestionRead(
            id=item.id,
            question=item.question,
            explanation=item.explanation,
            image=item.image,
            options=item.options,
        )
