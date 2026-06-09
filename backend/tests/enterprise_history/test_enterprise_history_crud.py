from pathlib import Path

import pytest

from app.core.config import settings
from app.modules.enterprise_history.files import EnterpriseHistoryFileStorage
from app.modules.enterprise_history.models import (
    EnterpriseHistory,
    EnterpriseHistoryGalleryImage,
    EnterpriseHistorySlide,
)
from app.modules.users.models import UserRole
from tests.enterprise_history.helpers import (
    ENTERPRISE_HISTORY_API,
    assert_enterprise_history_admin_detail,
    assert_enterprise_history_admin_summary,
    assert_enterprise_history_public_detail,
    assert_enterprise_history_public_summary,
    build_image_file,
)
from tests.users.helpers import assert_detail_payload, auth_headers


@pytest.mark.asyncio
async def test_create_draft_enterprise_history(client, create_user, login):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    response = await client.post(
        ENTERPRISE_HISTORY_API,
        headers=auth_headers(token),
        data={
            "title": "Уралмаш",
            "subdistrict": "УКТУС",
            "general_subtitle": "Общий подзаголовок",
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert_enterprise_history_admin_detail(payload)
    assert payload["title"] == "Уралмаш"
    assert payload["subdistrict"] == "УКТУС"
    assert payload["is_draft"] is True


@pytest.mark.asyncio
async def test_create_published_enterprise_history(client, create_user, login):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    response = await client.post(
        ENTERPRISE_HISTORY_API,
        headers=auth_headers(token),
        data={
            "title": "Уралмаш",
            "subdistrict": "УКТУС",
            "general_subtitle": "Общий подзаголовок",
            "detail_subtitle": "Детальный подзаголовок",
            "short_description": "Краткое описание",
            "is_draft": "false",
        },
        files=[
            ("general_main_image", build_image_file("general.jpg")),
            ("detail_main_image", build_image_file("detail.jpg")),
        ],
    )

    assert response.status_code == 201
    payload = response.json()
    assert_enterprise_history_admin_detail(payload)
    assert payload["subdistrict"] == "УКТУС"
    assert payload["is_draft"] is False
    assert payload["general_main_image"].startswith(
        f"{settings.UPLOAD_URL_PREFIX}/enterprise_history/general_main/"
    )
    assert payload["detail_main_image"].startswith(
        f"{settings.UPLOAD_URL_PREFIX}/enterprise_history/detail_main/"
    )


@pytest.mark.asyncio
async def test_create_enterprise_history_accepts_gallery_images(
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
        ENTERPRISE_HISTORY_API,
        headers=auth_headers(token),
        data={
            "title": "Draft enterprise history",
        },
        files=[
            ("gallery", build_image_file("gallery1.jpg")),
            ("gallery", build_image_file("gallery2.jpg", b"gallery-two")),
        ],
    )

    assert response.status_code == 201
    payload = response.json()
    assert_enterprise_history_admin_detail(payload)
    assert len(payload["gallery"]) == 2
    assert payload["gallery"][0]["position"] == 0
    assert payload["gallery"][1]["position"] == 1
    assert payload["gallery"][0]["image"].startswith(
        f"{settings.UPLOAD_URL_PREFIX}/enterprise_history/gallery/"
    )


@pytest.mark.asyncio
async def test_create_enterprise_history_openapi_exposes_file_inputs(client):
    response = await client.get("/openapi.json")

    assert response.status_code == 200
    schema = response.json()["paths"][ENTERPRISE_HISTORY_API]["post"]["requestBody"][
        "content"
    ]["multipart/form-data"]["schema"]["properties"]
    assert schema["general_main_image"]["format"] == "binary"
    assert schema["detail_main_image"]["format"] == "binary"
    assert schema["gallery"]["type"] == "array"
    assert schema["gallery"]["items"]["format"] == "binary"


@pytest.mark.asyncio
async def test_public_list_and_detail_return_published_enterprise_history(
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
        ENTERPRISE_HISTORY_API,
        headers=auth_headers(token),
        data={
            "title": "Уралмаш",
            "subdistrict": "УКТУС",
            "general_subtitle": "Общий подзаголовок",
            "detail_subtitle": "Детальный подзаголовок",
            "short_description": "Краткое описание",
            "is_draft": "false",
        },
        files=[
            ("general_main_image", build_image_file("general.jpg")),
            ("detail_main_image", build_image_file("detail.jpg")),
        ],
    )
    item_id = created.json()["id"]

    added_slide = await client.post(
        f"{ENTERPRISE_HISTORY_API}/{item_id}/how-it-was",
        headers=auth_headers(token),
        data={"text": "Первый слайд"},
    )
    assert added_slide.status_code == 200

    added_gallery = await client.post(
        f"{ENTERPRISE_HISTORY_API}/{item_id}/gallery",
        headers=auth_headers(token),
        files=[("images", build_image_file("gallery.jpg"))],
    )
    assert added_gallery.status_code == 200

    list_response = await client.get(ENTERPRISE_HISTORY_API)
    assert list_response.status_code == 200
    list_payload = list_response.json()
    assert len(list_payload) == 1
    assert_enterprise_history_public_summary(list_payload[0])
    assert list_payload[0]["subdistrict"] == "УКТУС"
    assert list_payload[0]["subtitle"] == "Общий подзаголовок"

    detail_response = await client.get(f"{ENTERPRISE_HISTORY_API}/{item_id}")
    assert detail_response.status_code == 200
    detail_payload = detail_response.json()
    assert_enterprise_history_public_detail(detail_payload)
    assert detail_payload["subdistrict"] == "УКТУС"
    assert detail_payload["subtitle"] == "Детальный подзаголовок"
    assert len(detail_payload["how_it_was"]) == 1
    assert len(detail_payload["gallery"]) == 1


@pytest.mark.asyncio
async def test_admin_list_contains_drafts(client, create_user, login):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    token = await login(email="admin@example.com", password="AdminPass123")

    await client.post(
        ENTERPRISE_HISTORY_API,
        headers=auth_headers(token),
        data={"title": "Черновик", "subdistrict": "ХИММАШ"},
    )

    response = await client.get(
        f"{ENTERPRISE_HISTORY_API}/admin",
        headers=auth_headers(token),
    )

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert_enterprise_history_admin_summary(payload[0])
    assert payload[0]["subdistrict"] == "ХИММАШ"
    assert payload[0]["is_draft"] is True


@pytest.mark.asyncio
async def test_enterprise_history_slides_and_gallery_can_be_managed(
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
        ENTERPRISE_HISTORY_API,
        headers=auth_headers(token),
        data={"title": "Черновик", "subdistrict": "УКТУС"},
    )
    item_id = created.json()["id"]

    first_slide = await client.post(
        f"{ENTERPRISE_HISTORY_API}/{item_id}/how-it-was",
        headers=auth_headers(token),
        data={"text": "Только текст"},
    )
    assert first_slide.status_code == 200
    first_payload = first_slide.json()
    slide_ids = [item["id"] for item in first_payload["how_it_was"]]
    assert len(slide_ids) == 1

    second_slide = await client.post(
        f"{ENTERPRISE_HISTORY_API}/{item_id}/how-it-was",
        headers=auth_headers(token),
        data={"order_index": "0"},
        files=[("image", build_image_file("slide.jpg"))],
    )
    assert second_slide.status_code == 200
    second_payload = second_slide.json()
    assert_enterprise_history_admin_detail(second_payload)
    slide_ids = [item["id"] for item in second_payload["how_it_was"]]
    assert len(slide_ids) == 2
    assert second_payload["how_it_was"][0]["image"] is not None

    reordered = await client.put(
        f"{ENTERPRISE_HISTORY_API}/{item_id}/how-it-was/order",
        headers=auth_headers(token),
        json={"slide_ids": [slide_ids[1], slide_ids[0]]},
    )
    assert reordered.status_code == 200
    reordered_payload = reordered.json()
    assert [item["id"] for item in reordered_payload["how_it_was"]] == [
        slide_ids[1],
        slide_ids[0],
    ]

    gallery_added = await client.post(
        f"{ENTERPRISE_HISTORY_API}/{item_id}/gallery",
        headers=auth_headers(token),
        files=[
            ("images", build_image_file("gallery1.jpg")),
            ("images", build_image_file("gallery2.jpg", b"gallery-two")),
        ],
    )
    assert gallery_added.status_code == 200
    gallery_payload = gallery_added.json()
    gallery_ids = [item["id"] for item in gallery_payload["gallery"]]
    assert len(gallery_ids) == 2

    gallery_reordered = await client.put(
        f"{ENTERPRISE_HISTORY_API}/{item_id}/gallery/order",
        headers=auth_headers(token),
        json={"image_ids": [gallery_ids[1], gallery_ids[0]]},
    )
    assert gallery_reordered.status_code == 200
    reordered_gallery_payload = gallery_reordered.json()
    assert [item["id"] for item in reordered_gallery_payload["gallery"]] == [
        gallery_ids[1],
        gallery_ids[0],
    ]

    removed_slide = await client.delete(
        f"{ENTERPRISE_HISTORY_API}/{item_id}/how-it-was/{slide_ids[0]}",
        headers=auth_headers(token),
    )
    assert removed_slide.status_code == 200
    assert len(removed_slide.json()["how_it_was"]) == 1

    removed_gallery = await client.delete(
        f"{ENTERPRISE_HISTORY_API}/{item_id}/gallery/{gallery_ids[0]}",
        headers=auth_headers(token),
    )
    assert removed_gallery.status_code == 200
    assert len(removed_gallery.json()["gallery"]) == 1


@pytest.mark.asyncio
async def test_delete_enterprise_history_removes_db_rows_and_files(
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
        ENTERPRISE_HISTORY_API,
        headers=auth_headers(token),
        data={
            "title": "Уралмаш",
            "subdistrict": "УКТУС",
            "general_subtitle": "Общий подзаголовок",
            "detail_subtitle": "Детальный подзаголовок",
            "short_description": "Краткое описание",
            "is_draft": "false",
        },
        files=[
            ("general_main_image", build_image_file("general.jpg")),
            ("detail_main_image", build_image_file("detail.jpg")),
        ],
    )
    item_id = created.json()["id"]

    slide_added = await client.post(
        f"{ENTERPRISE_HISTORY_API}/{item_id}/how-it-was",
        headers=auth_headers(token),
        files=[("image", build_image_file("slide.jpg"))],
    )
    gallery_added = await client.post(
        f"{ENTERPRISE_HISTORY_API}/{item_id}/gallery",
        headers=auth_headers(token),
        files=[("images", build_image_file("gallery.jpg"))],
    )
    payload = gallery_added.json()

    file_storage = EnterpriseHistoryFileStorage()
    general_file = (
        file_storage.general_main_dir / Path(payload["general_main_image"]).name
    )
    detail_file = file_storage.detail_main_dir / Path(payload["detail_main_image"]).name
    slide_file = (
        file_storage.how_it_was_dir
        / Path(slide_added.json()["how_it_was"][0]["image"]).name
    )
    gallery_file = file_storage.gallery_dir / Path(payload["gallery"][0]["image"]).name
    assert general_file.exists()
    assert detail_file.exists()
    assert slide_file.exists()
    assert gallery_file.exists()

    response = await client.delete(
        f"{ENTERPRISE_HISTORY_API}/{item_id}",
        headers=auth_headers(token),
    )

    assert response.status_code == 200

    async with db_session_factory() as session:
        assert await session.get(EnterpriseHistory, item_id) is None
        assert (
            await session.get(
                EnterpriseHistorySlide, slide_added.json()["how_it_was"][0]["id"]
            )
            is None
        )
        assert (
            await session.get(
                EnterpriseHistoryGalleryImage,
                payload["gallery"][0]["id"],
            )
            is None
        )

    assert not general_file.exists()
    assert not detail_file.exists()
    assert not slide_file.exists()
    assert not gallery_file.exists()


@pytest.mark.asyncio
async def test_publish_requires_subdistrict_subtitles_and_images(
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
        ENTERPRISE_HISTORY_API,
        headers=auth_headers(token),
        data={"title": "Уралмаш", "subdistrict": "УКТУС", "is_draft": "false"},
    )

    assert response.status_code == 422
    assert_detail_payload(response.json())


@pytest.mark.asyncio
async def test_public_enterprise_history_list_can_be_filtered_by_subdistrict(
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

    for subdistrict in ("УКТУС", "ХИММАШ"):
        response = await client.post(
            ENTERPRISE_HISTORY_API,
            headers=auth_headers(token),
            data={
                "title": f"Предприятие {subdistrict}",
                "subdistrict": subdistrict,
                "general_subtitle": "Общий подзаголовок",
                "detail_subtitle": "Детальный подзаголовок",
                "short_description": "Краткое описание",
                "is_draft": "false",
            },
            files=[
                ("general_main_image", build_image_file(f"{subdistrict}-general.jpg")),
                ("detail_main_image", build_image_file(f"{subdistrict}-detail.jpg")),
            ],
        )
        assert response.status_code == 201

    filtered_response = await client.get(f"{ENTERPRISE_HISTORY_API}?subdistrict=УКТУС")

    assert filtered_response.status_code == 200
    payload = filtered_response.json()
    assert len(payload) == 1
    assert payload[0]["subdistrict"] == "УКТУС"
