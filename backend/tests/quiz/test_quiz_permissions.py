import pytest

from app.modules.users.models import UserRole
from tests.quiz.helpers import QUIZ_API, build_image_file
from tests.users.helpers import assert_detail_payload, auth_headers


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("method", "path", "kwargs"),
    [
        (
            "post",
            QUIZ_API,
            {
                "json": {
                    "question": "Вопрос",
                    "options": [
                        {"text": "Да", "is_correct": True},
                        {"text": "Нет", "is_correct": False},
                    ],
                }
            },
        ),
        ("patch", f"{QUIZ_API}/1", {"json": {"question": "Новый"}}),
        ("put", f"{QUIZ_API}/1/image", {"files": build_image_file("quiz.jpg")}),
        ("delete", f"{QUIZ_API}/1/image", {}),
        ("delete", f"{QUIZ_API}/1", {}),
    ],
)
async def test_mutating_quiz_endpoints_require_auth(
    client,
    method: str,
    path: str,
    kwargs: dict,
):
    response = await getattr(client, method)(path, **kwargs)

    assert response.status_code == 401
    assert_detail_payload(response.json())


@pytest.mark.asyncio
async def test_public_quiz_endpoints_do_not_require_auth(client, create_user, login):
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
            "question": "Публичный вопрос",
            "options": [
                {"text": "Да", "is_correct": True},
                {"text": "Нет", "is_correct": False},
            ],
        },
    )
    item_id = created.json()["id"]

    list_response = await client.get(QUIZ_API)
    detail_response = await client.get(f"{QUIZ_API}/{item_id}")

    assert list_response.status_code == 200
    assert detail_response.status_code == 200


@pytest.mark.asyncio
async def test_quiz_detail_returns_404_for_missing_question(client):
    response = await client.get(f"{QUIZ_API}/9999")

    assert response.status_code == 404
    assert_detail_payload(response.json())


@pytest.mark.asyncio
async def test_upload_quiz_image_rejects_non_image_file(client, create_user, login):
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
            "question": "Вопрос",
            "options": [
                {"text": "Да", "is_correct": True},
                {"text": "Нет", "is_correct": False},
            ],
        },
    )
    item_id = created.json()["id"]

    response = await client.put(
        f"{QUIZ_API}/{item_id}/image",
        headers=auth_headers(token),
        files={"image": ("notes.txt", b"text-file", "text/plain")},
    )

    assert response.status_code == 400
    assert_detail_payload(response.json())
