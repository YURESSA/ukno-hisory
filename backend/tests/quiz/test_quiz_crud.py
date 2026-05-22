from pathlib import Path

import pytest

from app.core.config import settings
from app.modules.quiz.files import QuizFileStorage
from app.modules.quiz.models import QuizQuestion, QuizQuestionOption
from app.modules.users.models import UserRole
from tests.quiz.helpers import QUIZ_API, assert_quiz_payload, build_image_file
from tests.users.helpers import assert_detail_payload, auth_headers


def build_options() -> list[dict]:
    return [
        {"text": "Ответ 1", "is_correct": False},
        {"text": "Ответ 2", "is_correct": True},
        {"text": "Ответ 3", "is_correct": False},
    ]


@pytest.mark.asyncio
async def test_create_quiz_question(client, create_user, login):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    response = await client.post(
        QUIZ_API,
        headers=auth_headers(token),
        json={
            "question": "Какой вариант правильный?",
            "explanation": "Правильный ответ второй",
            "options": build_options(),
        },
    )

    assert response.status_code == 201
    assert_quiz_payload(
        response.json(),
        question="Какой вариант правильный?",
        explanation="Правильный ответ второй",
        image=None,
        options=build_options(),
    )


@pytest.mark.asyncio
async def test_create_quiz_question_with_image(client, create_user, login):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    response = await client.post(
        QUIZ_API,
        headers=auth_headers(token),
        data={
            "question": "Вопрос с картинкой",
            "explanation": "Пояснение",
            "options": (
                '[{"text":"Ответ 1","is_correct":false},'
                '{"text":"Ответ 2","is_correct":true}]'
            ),
        },
        files=build_image_file("quiz.jpg"),
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["image"].startswith(f"{settings.UPLOAD_URL_PREFIX}/quiz/")
    assert_quiz_payload(
        payload,
        question="Вопрос с картинкой",
        explanation="Пояснение",
        image=payload["image"],
        options=[
            {"text": "Ответ 1", "is_correct": False},
            {"text": "Ответ 2", "is_correct": True},
        ],
    )


@pytest.mark.asyncio
async def test_get_quiz_questions(client, create_user, login):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    await client.post(
        QUIZ_API,
        headers=auth_headers(token),
        json={
            "question": "Первый вопрос",
            "options": build_options(),
        },
    )
    await client.post(
        QUIZ_API,
        headers=auth_headers(token),
        json={
            "question": "Второй вопрос",
            "options": [
                {"text": "Да", "is_correct": True},
                {"text": "Нет", "is_correct": False},
            ],
        },
    )

    response = await client.get(QUIZ_API)

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 2
    assert payload[0]["question"] == "Первый вопрос"
    assert payload[1]["question"] == "Второй вопрос"


@pytest.mark.asyncio
async def test_get_quiz_question_detail(client, create_user, login):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    created = await client.post(
        QUIZ_API,
        headers=auth_headers(token),
        json={
            "question": "Вопрос для detail",
            "explanation": "Подсказка",
            "options": build_options(),
        },
    )
    item_id = created.json()["id"]

    response = await client.get(f"{QUIZ_API}/{item_id}")

    assert response.status_code == 200
    assert_quiz_payload(
        response.json(),
        question="Вопрос для detail",
        explanation="Подсказка",
        image=None,
        options=build_options(),
    )


@pytest.mark.asyncio
async def test_update_quiz_question_replaces_options(client, create_user, login):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    created = await client.post(
        QUIZ_API,
        headers=auth_headers(token),
        json={
            "question": "Старый вопрос",
            "explanation": "Старое пояснение",
            "options": build_options(),
        },
    )
    item_id = created.json()["id"]

    updated_options = [
        {"text": "Новый 1", "is_correct": True},
        {"text": "Новый 2", "is_correct": False},
    ]
    response = await client.patch(
        f"{QUIZ_API}/{item_id}",
        headers=auth_headers(token),
        json={
            "question": "Новый вопрос",
            "explanation": None,
            "options": updated_options,
        },
    )

    assert response.status_code == 200
    assert_quiz_payload(
        response.json(),
        question="Новый вопрос",
        explanation=None,
        image=None,
        options=updated_options,
    )


@pytest.mark.asyncio
async def test_update_quiz_question_image(client, create_user, login):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    created = await client.post(
        QUIZ_API,
        headers=auth_headers(token),
        json={"question": "С картинкой", "options": build_options()},
    )
    item_id = created.json()["id"]

    response = await client.put(
        f"{QUIZ_API}/{item_id}/image",
        headers=auth_headers(token),
        files=build_image_file("quiz.jpg"),
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["image"].startswith(f"{settings.UPLOAD_URL_PREFIX}/quiz/")
    assert_quiz_payload(
        payload,
        question="С картинкой",
        explanation=None,
        image=payload["image"],
        options=build_options(),
    )


@pytest.mark.asyncio
async def test_delete_quiz_question_image(client, create_user, login):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    created = await client.post(
        QUIZ_API,
        headers=auth_headers(token),
        json={"question": "С картинкой", "options": build_options()},
    )
    item_id = created.json()["id"]
    await client.put(
        f"{QUIZ_API}/{item_id}/image",
        headers=auth_headers(token),
        files=build_image_file("quiz.jpg"),
    )

    response = await client.delete(
        f"{QUIZ_API}/{item_id}/image",
        headers=auth_headers(token),
    )

    assert response.status_code == 200
    assert_quiz_payload(
        response.json(),
        question="С картинкой",
        explanation=None,
        image=None,
        options=build_options(),
    )


@pytest.mark.asyncio
async def test_delete_quiz_question_removes_db_rows_and_file(
    client,
    create_user,
    login,
    db_session_factory,
):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    created = await client.post(
        QUIZ_API,
        headers=auth_headers(token),
        json={"question": "Удаляемый вопрос", "options": build_options()},
    )
    item_id = created.json()["id"]
    with_image = await client.put(
        f"{QUIZ_API}/{item_id}/image",
        headers=auth_headers(token),
        files=build_image_file("quiz.jpg"),
    )
    payload = with_image.json()

    file_storage = QuizFileStorage()
    stored_file = file_storage.quiz_dir / Path(payload["image"]).name
    assert stored_file.exists()
    option_ids = [option["id"] for option in payload["options"]]

    response = await client.delete(
        f"{QUIZ_API}/{item_id}",
        headers=auth_headers(token),
    )

    assert response.status_code == 200
    assert_detail_payload(response.json())

    async with db_session_factory() as session:
        assert await session.get(QuizQuestion, item_id) is None
        for option_id in option_ids:
            assert await session.get(QuizQuestionOption, option_id) is None

    assert not stored_file.exists()


@pytest.mark.asyncio
async def test_create_quiz_question_requires_two_options(client, create_user, login):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    response = await client.post(
        QUIZ_API,
        headers=auth_headers(token),
        json={
            "question": "Недостаточно вариантов",
            "options": [{"text": "Только один", "is_correct": True}],
        },
    )

    assert response.status_code == 422
    assert_detail_payload(response.json())


@pytest.mark.asyncio
async def test_create_quiz_question_requires_exactly_one_correct_answer(
    client,
    create_user,
    login,
):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    response = await client.post(
        QUIZ_API,
        headers=auth_headers(token),
        json={
            "question": "Сколько правильных?",
            "options": [
                {"text": "Один", "is_correct": True},
                {"text": "Два", "is_correct": True},
            ],
        },
    )

    assert response.status_code == 422
    assert_detail_payload(response.json())


@pytest.mark.asyncio
async def test_update_quiz_question_requires_at_least_one_field(
    client,
    create_user,
    login,
):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    created = await client.post(
        QUIZ_API,
        headers=auth_headers(token),
        json={"question": "Пустой patch", "options": build_options()},
    )
    item_id = created.json()["id"]

    response = await client.patch(
        f"{QUIZ_API}/{item_id}",
        headers=auth_headers(token),
        json={},
    )

    assert response.status_code == 422
    assert_detail_payload(response.json())


@pytest.mark.asyncio
async def test_upload_quiz_question_image_rejects_empty_file(
    client, create_user, login
):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    created = await client.post(
        QUIZ_API,
        headers=auth_headers(token),
        json={"question": "Пустой файл", "options": build_options()},
    )
    item_id = created.json()["id"]

    response = await client.put(
        f"{QUIZ_API}/{item_id}/image",
        headers=auth_headers(token),
        files=build_image_file("empty.jpg", b""),
    )

    assert response.status_code == 400
    assert_detail_payload(response.json())
