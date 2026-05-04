import pytest

from app.modules.users.models import UserRole
from tests.timeline.helpers import TIMELINE_API
from tests.users.helpers import assert_detail_payload, auth_headers


def build_image_file(name: str, content: bytes = b"fake-image-content") -> dict:
    return {"image": (name, content, "image/jpeg")}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("method", "path", "body", "files"),
    [
        (
            "post",
            TIMELINE_API,
            {"year": "1991", "text": "Event"},
            build_image_file("event.jpg"),
        ),
        (
            "put",
            f"{TIMELINE_API}/1",
            {"year": "1992", "text": "Updated"},
            build_image_file("updated.jpg"),
        ),
        ("delete", f"{TIMELINE_API}/1", None, None),
    ],
)
async def test_mutating_timeline_endpoints_require_auth(
    client,
    method: str,
    path: str,
    body: dict | None,
    files: dict | None,
):
    request_kwargs = {}
    if body is not None:
        request_kwargs["data"] = body
    if files is not None:
        request_kwargs["files"] = files

    response = await getattr(client, method)(path, **request_kwargs)

    assert response.status_code == 401
    assert_detail_payload(response.json())


@pytest.mark.asyncio
async def test_public_timeline_endpoints_do_not_require_auth(
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
        TIMELINE_API,
        headers=auth_headers(token),
        data={"year": "1991", "text": "Event"},
        files=build_image_file("event.jpg"),
    )
    entry_id = created.json()["id"]

    list_response = await client.get(TIMELINE_API)
    detail_response = await client.get(f"{TIMELINE_API}/{entry_id}")

    assert list_response.status_code == 200
    assert detail_response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.parametrize("method", ["post", "put", "delete"])
async def test_mutating_timeline_endpoints_available_for_superadmin_too(
    client,
    create_user,
    login,
    method: str,
):
    await create_user(
        email="root@example.com",
        password="RootPass123",
        role=UserRole.SUPERADMIN,
    )
    token = await login(email="root@example.com", password="RootPass123")

    created = await client.post(
        TIMELINE_API,
        headers=auth_headers(token),
        data={"year": "1991", "text": "Event"},
        files=build_image_file("event.jpg"),
    )
    entry_id = created.json()["id"]

    if method == "post":
        response = await client.post(
            TIMELINE_API,
            headers=auth_headers(token),
            data={"year": "1992", "text": "Second"},
            files=build_image_file("second.jpg"),
        )
        assert response.status_code == 201
        return

    if method == "put":
        response = await client.put(
            f"{TIMELINE_API}/{entry_id}",
            headers=auth_headers(token),
            data={"year": "1993", "text": "Updated"},
            files=build_image_file("updated.jpg"),
        )
        assert response.status_code == 200
        return

    response = await client.delete(
        f"{TIMELINE_API}/{entry_id}",
        headers=auth_headers(token),
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_timeline_detail_returns_404_for_missing_entry(client):
    response = await client.get(f"{TIMELINE_API}/9999")

    assert response.status_code == 404
    assert_detail_payload(response.json())


@pytest.mark.asyncio
async def test_create_timeline_entry_rejects_non_image_file(
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
        TIMELINE_API,
        headers=auth_headers(token),
        data={"year": "1991", "text": "Event"},
        files={"image": ("notes.txt", b"text-file", "text/plain")},
    )

    assert response.status_code == 400
    assert_detail_payload(response.json())
