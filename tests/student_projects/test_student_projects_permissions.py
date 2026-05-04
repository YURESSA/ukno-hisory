import pytest

from app.modules.users.models import UserRole
from tests.student_projects.helpers import (
    PROJECTS_API,
    assert_student_project_admin_detail,
)
from tests.users.helpers import assert_detail_payload, auth_headers


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("method", "path", "kwargs"),
    [
        ("post", PROJECTS_API, {"data": {"title": "Draft only"}}),
        ("put", f"{PROJECTS_API}/1", {"data": {"title": "Changed"}}),
        ("delete", f"{PROJECTS_API}/1", {}),
        (
            "post",
            f"{PROJECTS_API}/1/gallery",
            {"files": [("images", ("a.jpg", b"x", "image/jpeg"))]},
        ),
        ("delete", f"{PROJECTS_API}/1/gallery/1", {}),
        (
            "put",
            f"{PROJECTS_API}/1/gallery/order",
            {"json": {"image_ids": [1]}},
        ),
        ("get", f"{PROJECTS_API}/admin", {}),
        ("get", f"{PROJECTS_API}/admin/1", {}),
    ],
)
async def test_admin_student_project_endpoints_require_auth(
    client,
    method: str,
    path: str,
    kwargs: dict,
):
    response = await getattr(client, method)(path, **kwargs)

    assert response.status_code == 401
    assert_detail_payload(response.json())


@pytest.mark.asyncio
async def test_public_detail_hides_draft_project(client, create_user, login):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    created = await client.post(
        PROJECTS_API,
        headers=auth_headers(token),
        data={"title": "Draft only"},
    )
    project_id = created.json()["id"]

    response = await client.get(f"{PROJECTS_API}/{project_id}")

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
        PROJECTS_API,
        headers=auth_headers(token),
        data={"title": "Draft only"},
    )
    project_id = created.json()["id"]

    response = await client.get(
        f"{PROJECTS_API}/admin/{project_id}",
        headers=auth_headers(token),
    )

    assert response.status_code == 200
    payload = response.json()
    assert_student_project_admin_detail(payload)
    assert payload["is_draft"] is True


@pytest.mark.asyncio
async def test_create_published_project_requires_main_image(client, create_user, login):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    response = await client.post(
        PROJECTS_API,
        headers=auth_headers(token),
        data={
            "title": "Public project",
            "author": "Olga",
            "short_description": "Short summary",
            "description": "Long project description",
            "year": "2025",
            "is_draft": "false",
        },
    )

    assert response.status_code == 422
    assert_detail_payload(response.json())


@pytest.mark.asyncio
async def test_update_project_requires_some_fields(client, create_user, login):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    created = await client.post(
        PROJECTS_API,
        headers=auth_headers(token),
        data={"title": "Draft only"},
    )
    project_id = created.json()["id"]

    response = await client.put(
        f"{PROJECTS_API}/{project_id}",
        headers=auth_headers(token),
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
        PROJECTS_API,
        headers=auth_headers(token),
        data={"title": "Draft only"},
    )
    project_id = created.json()["id"]

    response = await client.post(
        f"{PROJECTS_API}/{project_id}/gallery",
        headers=auth_headers(token),
        files=[("images", ("notes.txt", b"text", "text/plain"))],
    )

    assert response.status_code == 400
    assert_detail_payload(response.json())


@pytest.mark.asyncio
async def test_empty_gallery_upload_rejected(client, create_user, login):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    created = await client.post(
        PROJECTS_API,
        headers=auth_headers(token),
        data={"title": "Draft only"},
    )
    project_id = created.json()["id"]

    response = await client.post(
        f"{PROJECTS_API}/{project_id}/gallery",
        headers=auth_headers(token),
        files=[("images", ("empty.jpg", b"", "image/jpeg"))],
    )

    assert response.status_code == 400
    assert_detail_payload(response.json())
