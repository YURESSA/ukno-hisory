import pytest
from sqlalchemy.exc import IntegrityError

from app.core.config import settings
from app.modules.timeline.files import TimelineFileStorage
from app.modules.timeline.models import TimelineEntry
from app.modules.users.models import UserRole
from tests.timeline.helpers import TIMELINE_API, assert_timeline_payload
from tests.users.helpers import assert_detail_payload, auth_headers


def build_image_file(name: str, content: bytes = b"fake-image-content") -> dict:
    return {"image": (name, content, "image/jpeg")}


@pytest.mark.asyncio
async def test_create_timeline_entry(client, create_user, login):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    response = await client.post(
        TIMELINE_API,
        headers=auth_headers(token),
        data={"year": "1991", "text": "Important event"},
        files=build_image_file("timeline.jpg"),
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["image"].startswith(f"{settings.UPLOAD_URL_PREFIX}/timeline/")
    assert_timeline_payload(
        payload,
        year=1991,
        image=payload["image"],
        text="Important event",
    )


@pytest.mark.asyncio
async def test_get_timeline_entries_returns_sorted_list(client, create_user, login):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    await client.post(
        TIMELINE_API,
        headers=auth_headers(token),
        data={"year": "2000", "text": "Later"},
        files=build_image_file("later.jpg"),
    )
    await client.post(
        TIMELINE_API,
        headers=auth_headers(token),
        data={"year": "1990", "text": "Earlier"},
        files=build_image_file("earlier.jpg"),
    )

    response = await client.get(TIMELINE_API)

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 2
    assert [item["year"] for item in payload] == [1990, 2000]


@pytest.mark.asyncio
async def test_get_timeline_entry_detail(client, create_user, login):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    created = await client.post(
        TIMELINE_API,
        headers=auth_headers(token),
        data={"year": "1939", "text": "Detail"},
        files=build_image_file("detail.jpg"),
    )
    entry_id = created.json()["id"]

    response = await client.get(f"{TIMELINE_API}/{entry_id}")

    assert response.status_code == 200
    payload = response.json()
    assert_timeline_payload(
        payload,
        year=1939,
        image=payload["image"],
        text="Detail",
    )


@pytest.mark.asyncio
async def test_update_timeline_entry(client, create_user, login):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    created = await client.post(
        TIMELINE_API,
        headers=auth_headers(token),
        data={"year": "1939", "text": "Detail"},
        files=build_image_file("detail.jpg"),
    )
    entry_id = created.json()["id"]
    old_image = created.json()["image"]

    response = await client.put(
        f"{TIMELINE_API}/{entry_id}",
        headers=auth_headers(token),
        data={"year": "1945", "text": "Updated detail"},
        files=build_image_file("updated.jpg", b"updated-image-content"),
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["image"] != old_image
    assert_timeline_payload(
        payload,
        year=1945,
        image=payload["image"],
        text="Updated detail",
    )


@pytest.mark.asyncio
async def test_update_timeline_entry_without_new_image_keeps_current_image(
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
        data={"year": "1939", "text": "Detail"},
        files=build_image_file("detail.jpg"),
    )
    entry_id = created.json()["id"]
    old_image = created.json()["image"]

    response = await client.put(
        f"{TIMELINE_API}/{entry_id}",
        headers=auth_headers(token),
        data={"year": "1941", "text": "Updated without image"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert_timeline_payload(
        payload,
        year=1941,
        image=old_image,
        text="Updated without image",
    )


@pytest.mark.asyncio
async def test_update_timeline_entry_only_year(client, create_user, login):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    created = await client.post(
        TIMELINE_API,
        headers=auth_headers(token),
        data={"year": "1939", "text": "Original text"},
        files=build_image_file("detail.jpg"),
    )
    entry_id = created.json()["id"]
    original_payload = created.json()

    response = await client.put(
        f"{TIMELINE_API}/{entry_id}",
        headers=auth_headers(token),
        data={"year": "1942"},
    )

    assert response.status_code == 200
    assert_timeline_payload(
        response.json(),
        year=1942,
        image=original_payload["image"],
        text="Original text",
    )


@pytest.mark.asyncio
async def test_update_timeline_entry_only_text(client, create_user, login):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    created = await client.post(
        TIMELINE_API,
        headers=auth_headers(token),
        data={"year": "1939", "text": "Original text"},
        files=build_image_file("detail.jpg"),
    )
    entry_id = created.json()["id"]
    original_payload = created.json()

    response = await client.put(
        f"{TIMELINE_API}/{entry_id}",
        headers=auth_headers(token),
        data={"text": "Updated only text"},
    )

    assert response.status_code == 200
    assert_timeline_payload(
        response.json(),
        year=1939,
        image=original_payload["image"],
        text="Updated only text",
    )


@pytest.mark.asyncio
async def test_update_timeline_entry_only_image(client, create_user, login):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    created = await client.post(
        TIMELINE_API,
        headers=auth_headers(token),
        data={"year": "1939", "text": "Original text"},
        files=build_image_file("detail.jpg"),
    )
    entry_id = created.json()["id"]
    original_payload = created.json()

    response = await client.put(
        f"{TIMELINE_API}/{entry_id}",
        headers=auth_headers(token),
        files=build_image_file("updated.jpg", b"updated-image-content"),
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["image"] != original_payload["image"]
    assert_timeline_payload(
        payload,
        year=1939,
        image=payload["image"],
        text="Original text",
    )


@pytest.mark.asyncio
async def test_delete_timeline_entry(client, create_user, login, db_session_factory):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    created = await client.post(
        TIMELINE_API,
        headers=auth_headers(token),
        data={"year": "1939", "text": "Detail"},
        files=build_image_file("detail.jpg"),
    )
    entry_id = created.json()["id"]
    image_path = created.json()["image"]
    file_storage = TimelineFileStorage()
    stored_file = file_storage.timeline_dir / image_path.rsplit("/", maxsplit=1)[-1]
    assert stored_file.exists()

    response = await client.delete(
        f"{TIMELINE_API}/{entry_id}",
        headers=auth_headers(token),
    )

    assert response.status_code == 200
    assert_detail_payload(response.json())

    async with db_session_factory() as session:
        assert await session.get(TimelineEntry, entry_id) is None
    assert not stored_file.exists()


@pytest.mark.asyncio
async def test_create_timeline_entry_rejects_invalid_year(client, create_user, login):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    response = await client.post(
        TIMELINE_API,
        headers=auth_headers(token),
        data={"year": "0", "text": "Invalid year"},
        files=build_image_file("timeline.jpg"),
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_timeline_entry_rejects_invalid_year_without_changing_data(
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
        data={"year": "1939", "text": "Detail"},
        files=build_image_file("detail.jpg"),
    )
    entry_id = created.json()["id"]
    original_payload = created.json()

    response = await client.put(
        f"{TIMELINE_API}/{entry_id}",
        headers=auth_headers(token),
        data={"year": "0", "text": "Should fail"},
    )

    assert response.status_code == 422

    detail_response = await client.get(f"{TIMELINE_API}/{entry_id}")
    assert detail_response.status_code == 200
    assert_timeline_payload(
        detail_response.json(),
        year=original_payload["year"],
        image=original_payload["image"],
        text=original_payload["text"],
    )


@pytest.mark.asyncio
async def test_update_timeline_entry_requires_at_least_one_field(
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
        data={"year": "1939", "text": "Detail"},
        files=build_image_file("detail.jpg"),
    )
    entry_id = created.json()["id"]

    response = await client.put(
        f"{TIMELINE_API}/{entry_id}",
        headers=auth_headers(token),
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_database_rejects_invalid_timeline_year(
    db_session_factory,
):
    async with db_session_factory() as session:
        session.add(
            TimelineEntry(
                year=0,
                image="/uploads/timeline/invalid.jpg",
                text="Invalid",
            )
        )
        with pytest.raises(IntegrityError):
            await session.commit()
