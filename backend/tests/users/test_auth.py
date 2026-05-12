import pytest

from tests.users.helpers import (
    AUTH_API,
    USERS_API,
    assert_detail_payload,
    assert_token_payload,
)


@pytest.mark.asyncio
async def test_users_login_success(client, create_user):
    await create_user(email="user@example.com", password="Secret123")

    response = await client.post(
        f"{USERS_API}/login",
        json={"email": "user@example.com", "password": "Secret123"},
    )

    assert response.status_code == 200
    assert_token_payload(response.json())


@pytest.mark.asyncio
async def test_users_login_invalid_credentials(client):
    response = await client.post(
        f"{USERS_API}/login",
        json={"email": "missing@example.com", "password": "wrong-pass"},
    )

    assert response.status_code == 401
    assert_detail_payload(response.json())


@pytest.mark.asyncio
async def test_auth_login_success(client, create_user):
    await create_user(email="oauth@example.com", password="FormPass123")

    response = await client.post(
        f"{AUTH_API}/login",
        data={"username": "oauth@example.com", "password": "FormPass123"},
    )

    assert response.status_code == 200
    assert_token_payload(response.json())
