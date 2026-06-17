import pytest

from app.core.config import settings
from app.modules.users.models import UserRole
from tests.enterprise_history.helpers import ENTERPRISE_HISTORY_API, build_image_file
from tests.users.helpers import assert_detail_payload, auth_headers

SUBDISTRICTS_API = "/api/v1/subdistricts"


@pytest.mark.asyncio
async def test_subdistrict_list_returns_predefined_items(client):
    response = await client.get(SUBDISTRICTS_API)

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 16
    assert payload[0]["name"] == "ВЕРХНЕМАКАРОВСКИЙ"
    assert set(payload[0]) == {"name", "description", "image"}


@pytest.mark.asyncio
async def test_subdistrict_detail_returns_description_image_and_enterprises(
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

    update_response = await client.patch(
        f"{SUBDISTRICTS_API}/УКТУС",
        headers=auth_headers(token),
        json={"description": "Описание подрайона"},
    )
    assert update_response.status_code == 200

    image_response = await client.put(
        f"{SUBDISTRICTS_API}/УКТУС/image",
        headers=auth_headers(token),
        files={"image": build_image_file("subdistrict.jpg")},
    )
    assert image_response.status_code == 200
    assert image_response.json()["image"].startswith(
        f"{settings.UPLOAD_URL_PREFIX}/subdistricts/images/"
    )

    created = await client.post(
        ENTERPRISE_HISTORY_API,
        headers=auth_headers(token),
        data={
            "title": "Завод на Уктусе",
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
    assert created.status_code == 201
    enterprise_id = created.json()["id"]

    detail_response = await client.get(f"{SUBDISTRICTS_API}/УКТУС")

    assert detail_response.status_code == 200
    payload = detail_response.json()
    assert payload["name"] == "УКТУС"
    assert payload["description"] == "Описание подрайона"
    assert isinstance(payload["image"], str)
    assert payload["enterprises"] == [{"id": enterprise_id, "title": "Завод на Уктусе"}]


@pytest.mark.asyncio
async def test_subdistrict_popularity_tracks_views_and_returns_leader(
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

    first_response = await client.get(f"{SUBDISTRICTS_API}/ШИННЫЙ")
    assert first_response.status_code == 200

    second_response = await client.get(f"{SUBDISTRICTS_API}/ШИННЫЙ")
    assert second_response.status_code == 200

    third_response = await client.get(f"{SUBDISTRICTS_API}/УКТУС")
    assert third_response.status_code == 200

    stats_response = await client.get(
        f"{SUBDISTRICTS_API}/popular",
        headers=auth_headers(token),
    )

    assert stats_response.status_code == 200
    payload = stats_response.json()
    assert payload["most_popular"] == {
        "name": "ШИННЫЙ",
        "views_count": 2,
    }
    assert payload["items"][0] == {
        "name": "ШИННЫЙ",
        "views_count": 2,
    }
    assert any(item == {"name": "УКТУС", "views_count": 1} for item in payload["items"])


@pytest.mark.asyncio
async def test_subdistrict_admin_endpoints_require_auth(client):
    response = await client.patch(
        f"{SUBDISTRICTS_API}/УКТУС",
        json={"description": "Описание"},
    )

    assert response.status_code == 401
    assert_detail_payload(response.json())

    popular_response = await client.get(f"{SUBDISTRICTS_API}/popular")
    assert popular_response.status_code == 401
    assert_detail_payload(popular_response.json())


@pytest.mark.asyncio
async def test_unknown_subdistrict_returns_404(client):
    response = await client.get(f"{SUBDISTRICTS_API}/НЕСУЩЕСТВУЮЩИЙ")

    assert response.status_code == 404
    assert_detail_payload(response.json())
