import pytest

from app.modules.users.models import UserRole
from tests.users.helpers import AUTH_API, assert_detail_payload, auth_headers

MAIN_SITE_TRANSITIONS_API = "/api/v1/main-site-transitions"


@pytest.mark.asyncio
async def test_track_main_site_transition_increments_counter(client):
    first_response = await client.post(MAIN_SITE_TRANSITIONS_API)

    assert first_response.status_code == 204
    assert first_response.content == b""

    second_response = await client.post(MAIN_SITE_TRANSITIONS_API)

    assert second_response.status_code == 204
    assert second_response.content == b""


@pytest.mark.asyncio
async def test_main_site_transition_stats_requires_admin(client):
    response = await client.get(f"{MAIN_SITE_TRANSITIONS_API}/stats")

    assert response.status_code == 401
    assert_detail_payload(response.json())


@pytest.mark.asyncio
async def test_admin_can_get_main_site_transition_stats(client, create_user):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    login_response = await client.post(
        f"{AUTH_API}/login",
        data={"username": "admin@example.com", "password": "AdminPass123"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    await client.post(MAIN_SITE_TRANSITIONS_API)
    await client.post(MAIN_SITE_TRANSITIONS_API)

    response = await client.get(
        f"{MAIN_SITE_TRANSITIONS_API}/stats",
        headers=auth_headers(token),
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["total_count"] == 2
    assert payload["latest_transition_at"] is not None
