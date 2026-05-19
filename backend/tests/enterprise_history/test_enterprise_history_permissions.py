import pytest

from app.modules.users.models import UserRole
from tests.enterprise_history.helpers import (
    ENTERPRISE_HISTORY_API,
    assert_enterprise_history_admin_detail,
)
from tests.users.helpers import assert_detail_payload, auth_headers


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("method", "path", "kwargs"),
    [
        ("post", ENTERPRISE_HISTORY_API, {"data": {"title": "Черновик"}}),
        ("patch", f"{ENTERPRISE_HISTORY_API}/1", {"json": {"title": "Изменено"}}),
        ("delete", f"{ENTERPRISE_HISTORY_API}/1", {}),
        ("post", f"{ENTERPRISE_HISTORY_API}/1/how-it-was", {"data": {"text": "Слайд"}}),
        ("delete", f"{ENTERPRISE_HISTORY_API}/1/how-it-was/1", {}),
        (
            "put",
            f"{ENTERPRISE_HISTORY_API}/1/how-it-was/order",
            {"json": {"slide_ids": [1]}},
        ),
        (
            "post",
            f"{ENTERPRISE_HISTORY_API}/1/gallery",
            {"files": [("images", ("a.jpg", b"x", "image/jpeg"))]},
        ),
        ("delete", f"{ENTERPRISE_HISTORY_API}/1/gallery/1", {}),
        (
            "put",
            f"{ENTERPRISE_HISTORY_API}/1/gallery/order",
            {"json": {"image_ids": [1]}},
        ),
        ("get", f"{ENTERPRISE_HISTORY_API}/admin", {}),
        ("get", f"{ENTERPRISE_HISTORY_API}/admin/1", {}),
    ],
)
async def test_admin_enterprise_history_endpoints_require_auth(
    client,
    method: str,
    path: str,
    kwargs: dict,
):
    response = await getattr(client, method)(path, **kwargs)

    assert response.status_code == 401
    assert_detail_payload(response.json())


@pytest.mark.asyncio
async def test_public_detail_hides_draft_enterprise_history(client, create_user, login):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    created = await client.post(
        ENTERPRISE_HISTORY_API,
        headers=auth_headers(token),
        data={"title": "Черновик"},
    )
    item_id = created.json()["id"]

    response = await client.get(f"{ENTERPRISE_HISTORY_API}/{item_id}")

    assert response.status_code == 404
    assert_detail_payload(response.json())


@pytest.mark.asyncio
async def test_admin_can_access_draft_detail(client, create_user, login):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    created = await client.post(
        ENTERPRISE_HISTORY_API,
        headers=auth_headers(token),
        data={"title": "Черновик"},
    )
    item_id = created.json()["id"]

    response = await client.get(
        f"{ENTERPRISE_HISTORY_API}/admin/{item_id}",
        headers=auth_headers(token),
    )

    assert response.status_code == 200
    payload = response.json()
    assert_enterprise_history_admin_detail(payload)
    assert payload["is_draft"] is True


@pytest.mark.asyncio
async def test_empty_slide_without_text_and_image_rejected(client, create_user, login):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    created = await client.post(
        ENTERPRISE_HISTORY_API,
        headers=auth_headers(token),
        data={"title": "Черновик"},
    )
    item_id = created.json()["id"]

    response = await client.post(
        f"{ENTERPRISE_HISTORY_API}/{item_id}/how-it-was",
        headers=auth_headers(token),
        data={},
    )

    assert response.status_code == 422
    assert_detail_payload(response.json())


@pytest.mark.asyncio
async def test_non_image_gallery_upload_rejected(client, create_user, login):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    created = await client.post(
        ENTERPRISE_HISTORY_API,
        headers=auth_headers(token),
        data={"title": "Черновик"},
    )
    item_id = created.json()["id"]

    response = await client.post(
        f"{ENTERPRISE_HISTORY_API}/{item_id}/gallery",
        headers=auth_headers(token),
        files=[("images", ("notes.txt", b"text", "text/plain"))],
    )

    assert response.status_code == 400
    assert_detail_payload(response.json())
