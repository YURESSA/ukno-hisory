import pytest

from app.core.config import settings
from app.modules.users.models import UserRole
from tests.student_projects.helpers import (
    PROJECTS_API,
    assert_student_project_admin_detail,
    build_image_file,
)
from tests.timeline.helpers import TIMELINE_API, assert_timeline_payload
from tests.users.helpers import auth_headers

pytestmark = pytest.mark.postgres_integration


@pytest.mark.asyncio
async def test_postgres_smoke_timeline_crud(client, create_user, login):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    created = await client.post(
        TIMELINE_API,
        headers=auth_headers(token),
        data={"year": "1961", "text": "Postgres timeline event"},
        files={"image": ("timeline.jpg", b"timeline-image", "image/jpeg")},
    )

    assert created.status_code == 201
    created_payload = created.json()
    assert created_payload["image"].startswith(
        f"{settings.UPLOAD_URL_PREFIX}/timeline/"
    )
    assert_timeline_payload(
        created_payload,
        year=1961,
        image=created_payload["image"],
        text="Postgres timeline event",
    )

    listed = await client.get(TIMELINE_API)

    assert listed.status_code == 200
    assert len(listed.json()) == 1


@pytest.mark.asyncio
async def test_postgres_smoke_student_project_gallery_flow(client, create_user, login):
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
            "title": "Postgres project",
            "author": "Infra",
            "short_description": "Smoke summary",
            "description": "Smoke description",
            "year": "2026",
            "is_draft": "false",
        },
        files=[("main_image", build_image_file("main.jpg"))],
    )

    assert created.status_code == 201
    payload = created.json()
    assert_student_project_admin_detail(payload)

    gallery_added = await client.post(
        f"{PROJECTS_API}/{payload['id']}/gallery",
        headers=auth_headers(token),
        files=[("images", build_image_file("gallery.jpg", b"gallery-image"))],
    )

    assert gallery_added.status_code == 200
    updated_payload = gallery_added.json()
    assert_student_project_admin_detail(updated_payload)
    assert len(updated_payload["gallery"]) == 1
