import pytest

from app.modules.users.models import User, UserRole
from tests.users.helpers import (
    USERS_API,
    assert_detail_payload,
    assert_user_payload,
    auth_headers,
)


@pytest.mark.asyncio
async def test_create_admin(client, create_user, login, sent_emails):
    await create_user(
        email="root@example.com",
        password="RootPass123",
        role=UserRole.SUPERADMIN,
    )
    token = await login(email="root@example.com", password="RootPass123")

    response = await client.post(
        f"{USERS_API}/create-admin",
        headers=auth_headers(token),
        json={"email": "new-admin@example.com"},
    )

    assert response.status_code == 201
    assert_user_payload(
        response.json(),
        email="new-admin@example.com",
        role=UserRole.ADMIN.value,
    )
    assert len(sent_emails) == 1
    assert sent_emails[0]["to"] == "new-admin@example.com"
    assert "AdminPass123" in sent_emails[0]["body"]


@pytest.mark.asyncio
async def test_get_users(client, create_user, login):
    await create_user(
        email="root@example.com",
        password="RootPass123",
        role=UserRole.SUPERADMIN,
    )
    await create_user(email="member@example.com", password="UserPass123")
    token = await login(email="root@example.com", password="RootPass123")

    response = await client.get(
        f"{USERS_API}/users",
        headers=auth_headers(token),
    )

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert len(payload) >= 2
    for user in payload:
        assert "id" in user
        assert "email" in user
        assert "role" in user
        assert isinstance(user["id"], int)
        assert isinstance(user["role"], str)
        assert user["role"]

    emails = {user["email"] for user in payload}
    assert {"root@example.com", "member@example.com"} <= emails


@pytest.mark.asyncio
async def test_get_user(client, create_user, login):
    await create_user(
        email="root@example.com",
        password="RootPass123",
        role=UserRole.SUPERADMIN,
    )
    target = await create_user(email="member@example.com", password="UserPass123")
    token = await login(email="root@example.com", password="RootPass123")

    response = await client.get(
        f"{USERS_API}/users/{target.id}",
        headers=auth_headers(token),
    )

    assert response.status_code == 200
    assert_user_payload(
        response.json(),
        email=target.email,
        role=UserRole.ADMIN.value,
    )


@pytest.mark.asyncio
async def test_delete_user(client, create_user, login, db_session_factory):
    await create_user(
        email="root@example.com",
        password="RootPass123",
        role=UserRole.SUPERADMIN,
    )
    target = await create_user(email="member@example.com", password="UserPass123")
    token = await login(email="root@example.com", password="RootPass123")

    response = await client.delete(
        f"{USERS_API}/users/{target.id}",
        headers=auth_headers(token),
    )

    assert response.status_code == 200
    assert_detail_payload(response.json())

    async with db_session_factory() as session:
        assert await session.get(User, target.id) is None
