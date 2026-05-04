from pathlib import Path

import pytest

from app.core.config import settings
from app.modules.student_projects.files import StudentProjectFileStorage
from app.modules.student_projects.models import (
    StudentProject,
    StudentProjectGalleryImage,
)
from app.modules.users.models import UserRole
from tests.student_projects.helpers import (
    PROJECTS_API,
    assert_student_project_admin_detail,
    assert_student_project_admin_summary,
    assert_student_project_public_detail,
    assert_student_project_public_summary,
    build_image_file,
)
from tests.users.helpers import assert_detail_payload, auth_headers


@pytest.mark.asyncio
async def test_create_draft_student_project(client, create_user, login):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    response = await client.post(
        PROJECTS_API,
        headers=auth_headers(token),
        data={"title": "Draft title"},
    )

    assert response.status_code == 201
    payload = response.json()
    assert_student_project_admin_detail(payload)
    assert payload["title"] == "Draft title"
    assert payload["is_draft"] is True
    assert payload["main_image"] is None


@pytest.mark.asyncio
async def test_create_published_student_project(client, create_user, login):
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
            "title": "Eco project",
            "author": "Ivan",
            "short_description": "Short summary",
            "description": "Long project description",
            "year": "2025",
            "tag_one": "Biology",
            "tag_two": "School",
            "is_draft": "false",
        },
        files=[("main_image", build_image_file("main.jpg"))],
    )

    assert response.status_code == 201
    payload = response.json()
    assert_student_project_admin_detail(payload)
    assert payload["is_draft"] is False
    assert payload["main_image"].startswith(
        f"{settings.UPLOAD_URL_PREFIX}/student_projects/main/"
    )
    assert len(payload["gallery"]) == 0


@pytest.mark.asyncio
async def test_get_public_student_projects_returns_only_published(
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

    await client.post(
        PROJECTS_API,
        headers=auth_headers(token),
        data={"title": "Draft only"},
    )
    await client.post(
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
        files=[("main_image", build_image_file("main.jpg"))],
    )

    response = await client.get(PROJECTS_API)

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert_student_project_public_summary(payload[0])
    assert payload[0]["title"] == "Public project"


@pytest.mark.asyncio
async def test_get_public_student_project_detail(client, create_user, login):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    created = await client.post(
        PROJECTS_API,
        headers=auth_headers(token),
        data={
            "title": "Public project",
            "author": "Olga",
            "short_description": "Short summary",
            "description": "Long project description",
            "year": "2025",
            "tag_one": "Math",
            "tag_two": "Research",
            "is_draft": "false",
        },
        files=[("main_image", build_image_file("main.jpg"))],
    )
    project_id = created.json()["id"]

    gallery_added = await client.post(
        f"{PROJECTS_API}/{project_id}/gallery",
        headers=auth_headers(token),
        files=[("images", build_image_file("gallery1.jpg"))],
    )
    assert gallery_added.status_code == 200

    response = await client.get(f"{PROJECTS_API}/{project_id}")

    assert response.status_code == 200
    payload = response.json()
    assert_student_project_public_detail(payload)
    assert payload["title"] == "Public project"
    assert payload["tags"]["author"] == "Olga"
    assert payload["tags"]["year"] == 2025
    assert len(payload["gallery"]) == 1


@pytest.mark.asyncio
async def test_admin_list_contains_drafts(client, create_user, login):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    await client.post(
        PROJECTS_API,
        headers=auth_headers(token),
        data={"title": "Draft only"},
    )

    response = await client.get(
        f"{PROJECTS_API}/admin",
        headers=auth_headers(token),
    )

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert_student_project_admin_summary(payload[0])
    assert payload[0]["is_draft"] is True


@pytest.mark.asyncio
async def test_update_student_project_any_fields(client, create_user, login):
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
        data={"author": "Petr", "description": "Filled later", "year": "2024"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert_student_project_admin_detail(payload)
    assert payload["title"] == "Draft only"
    assert payload["author"] == "Petr"
    assert payload["description"] == "Filled later"
    assert payload["year"] == 2024


@pytest.mark.asyncio
async def test_publish_draft_requires_all_required_fields(client, create_user, login):
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
        data={"is_draft": "false"},
    )

    assert response.status_code == 422
    assert_detail_payload(response.json())


@pytest.mark.asyncio
async def test_gallery_images_can_be_added_and_removed(client, create_user, login):
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

    first_added = await client.post(
        f"{PROJECTS_API}/{project_id}/gallery",
        headers=auth_headers(token),
        files=[
            ("images", build_image_file("gallery1.jpg")),
            ("images", build_image_file("gallery2.jpg", b"gallery-two")),
        ],
    )
    assert first_added.status_code == 200
    first_payload = first_added.json()
    assert_student_project_admin_detail(first_payload)
    gallery_ids = [item["id"] for item in first_payload["gallery"]]
    assert len(gallery_ids) == 2

    reordered = await client.put(
        f"{PROJECTS_API}/{project_id}/gallery/order",
        headers=auth_headers(token),
        json={"image_ids": [gallery_ids[1], gallery_ids[0]]},
    )
    assert reordered.status_code == 200
    reordered_payload = reordered.json()
    assert_student_project_admin_detail(reordered_payload)
    assert [item["id"] for item in reordered_payload["gallery"]] == [
        gallery_ids[1],
        gallery_ids[0],
    ]

    removed = await client.delete(
        f"{PROJECTS_API}/{project_id}/gallery/{gallery_ids[0]}",
        headers=auth_headers(token),
    )
    assert removed.status_code == 200
    removed_payload = removed.json()
    assert_student_project_admin_detail(removed_payload)
    assert len(removed_payload["gallery"]) == 1


@pytest.mark.asyncio
async def test_delete_student_project_removes_db_rows_and_files(
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
        files=[("main_image", build_image_file("main.jpg"))],
    )
    project_id = created.json()["id"]

    gallery_added = await client.post(
        f"{PROJECTS_API}/{project_id}/gallery",
        headers=auth_headers(token),
        files=[("images", build_image_file("gallery1.jpg"))],
    )
    payload = gallery_added.json()

    file_storage = StudentProjectFileStorage()
    main_file = file_storage.main_dir / Path(payload["main_image"]).name
    gallery_file = file_storage.gallery_dir / Path(payload["gallery"][0]["image"]).name
    assert main_file.exists()
    assert gallery_file.exists()

    response = await client.delete(
        f"{PROJECTS_API}/{project_id}",
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    async with db_session_factory() as session:
        assert await session.get(StudentProject, project_id) is None
        gallery_result = await session.get(
            StudentProjectGalleryImage,
            payload["gallery"][0]["id"],
        )
        assert gallery_result is None

    assert not main_file.exists()
    assert not gallery_file.exists()


@pytest.mark.asyncio
async def test_create_student_project_rejects_empty_main_image(
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
        PROJECTS_API,
        headers=auth_headers(token),
        data={"title": "Draft title"},
        files=[("main_image", build_image_file("empty.jpg", b""))],
    )

    assert response.status_code == 400
    assert_detail_payload(response.json())
