import json

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
    status,
)
from pydantic import ValidationError

from app.core.database import get_db
from app.core.dependencies import require_admin
from app.modules.quiz.files import QuizFileStorage
from app.modules.quiz.repository import QuizRepository
from app.modules.quiz.schemas import (
    QuizAdminStatsRead,
    QuizQuestionCreate,
    QuizQuestionRead,
    QuizQuestionUpdate,
    QuizSubmitRequest,
    QuizSubmitResultRead,
)
from app.modules.quiz.service import QuizService

router = APIRouter()


def get_service(db=Depends(get_db)):
    return QuizService(QuizRepository(db), QuizFileStorage())


@router.get(
    "",
    response_model=list[QuizQuestionRead],
    status_code=status.HTTP_200_OK,
    summary="Получить список вопросов квиза",
)
async def get_quiz_questions(service=Depends(get_service)):
    return await service.get_questions()


@router.post(
    "/submit",
    response_model=QuizSubmitResultRead,
    status_code=status.HTTP_200_OK,
    summary="Отправить ответы на квиз и получить результат",
)
async def submit_quiz(
    data: QuizSubmitRequest,
    service=Depends(get_service),
):
    return await service.submit_quiz(data)


@router.get(
    "/admin/stats",
    response_model=QuizAdminStatsRead,
    status_code=status.HTTP_200_OK,
    summary="Получить статистику прохождений квиза для администратора",
)
async def get_quiz_admin_stats(
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.get_admin_stats()


@router.get(
    "/{item_id}",
    response_model=QuizQuestionRead,
    status_code=status.HTTP_200_OK,
    summary="Получить вопрос квиза по идентификатору",
)
async def get_quiz_question(item_id: int, service=Depends(get_service)):
    return await service.get_question(item_id)


@router.post(
    "",
    response_model=QuizQuestionRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать вопрос квиза",
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "example": {
                        "question": "Столица России?",
                        "explanation": "Москва является столицей России.",
                        "options": [
                            {"text": "Париж", "is_correct": False},
                            {"text": "Москва", "is_correct": True},
                            {"text": "Берлин", "is_correct": False},
                        ],
                    }
                },
                "multipart/form-data": {
                    "schema": {
                        "type": "object",
                        "required": ["question", "options"],
                        "properties": {
                            "question": {
                                "type": "string",
                                "example": "Столица России?",
                            },
                            "explanation": {
                                "type": "string",
                                "example": "Москва является столицей России.",
                            },
                            "options": {
                                "type": "string",
                                "example": (
                                    '[{"text":"Париж","is_correct":false},'
                                    '{"text":"Москва","is_correct":true}]'
                                ),
                                "description": (
                                    "JSON-строка с массивом вариантов ответа"
                                ),
                            },
                            "image": {"type": "string", "format": "binary"},
                        },
                    }
                },
            }
        }
    },
)
async def create_quiz_question(
    request: Request,
    question: str | None = Form(None),
    explanation: str | None = Form(None),
    options: str | None = Form(None),
    image: UploadFile | None = File(None),
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    data = await _parse_create_payload(
        request=request,
        question=question,
        explanation=explanation,
        options=options,
    )
    return await service.create_question(data, image=image)


@router.patch(
    "/{item_id}",
    response_model=QuizQuestionRead,
    status_code=status.HTTP_200_OK,
    summary="Обновить вопрос квиза",
)
async def update_quiz_question(
    item_id: int,
    data: QuizQuestionUpdate,
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    if not data.model_fields_set:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Для обновления нужно передать хотя бы одно поле",
        )
    return await service.update_question(item_id, data)


@router.put(
    "/{item_id}/image",
    response_model=QuizQuestionRead,
    status_code=status.HTTP_200_OK,
    summary="Загрузить или заменить изображение вопроса квиза",
)
async def update_quiz_question_image(
    item_id: int,
    image: UploadFile = File(...),
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.update_question_image(item_id, image)


@router.delete(
    "/{item_id}/image",
    response_model=QuizQuestionRead,
    status_code=status.HTTP_200_OK,
    summary="Удалить изображение вопроса квиза",
)
async def delete_quiz_question_image(
    item_id: int,
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    return await service.delete_question_image(item_id)


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_200_OK,
    summary="Удалить вопрос квиза",
)
async def delete_quiz_question(
    item_id: int,
    service=Depends(get_service),
    _: None = Depends(require_admin),
):
    await service.delete_question(item_id)
    return {"detail": "Вопрос квиза удален"}


async def _parse_create_payload(
    *,
    request: Request,
    question: str | None,
    explanation: str | None,
    options: str | None,
) -> QuizQuestionCreate:
    content_type = request.headers.get("content-type", "")

    try:
        if "multipart/form-data" in content_type:
            parsed_options = json.loads(options) if options is not None else None
            payload = {
                "question": question,
                "explanation": explanation,
                "options": parsed_options,
            }
        else:
            payload = await request.json()

        return QuizQuestionCreate.model_validate(payload)
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Поле options должно быть валидным JSON-массивом",
        ) from exc
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(exc),
        ) from exc
