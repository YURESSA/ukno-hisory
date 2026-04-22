import pytest

from app.core.security import create_reset_token, verify_password
from app.modules.users.models import User, UserRole
from tests.users.conftest import LoginMode
from tests.users.helpers import USERS_API, assert_detail_payload, auth_headers


@pytest.mark.asyncio
async def test_change_password(client, create_user, login, db_session_factory):
    user = await create_user(
        email="admin@example.com",
        password="OldPass123",
        role=UserRole.ADMIN,
    )
    token = await login(
        email="admin@example.com",
        password="OldPass123",
        mode=LoginMode.JSON,
    )

    response = await client.post(
        f"{USERS_API}/change-password",
        headers=auth_headers(token),
        json={"old_password": "OldPass123", "new_password": "NewPass123"},
    )

    assert response.status_code == 200
    assert_detail_payload(response.json())

    async with db_session_factory() as session:
        updated_user = await session.get(User, user.id)
        assert updated_user is not None
        assert verify_password("NewPass123", updated_user.password_hash)


@pytest.mark.asyncio
async def test_change_password_rejects_wrong_old_password(
    client, create_user, login, db_session_factory
):
    user = await create_user(
        email="admin@example.com",
        password="OldPass123",
        role=UserRole.ADMIN,
    )
    token = await login(
        email="admin@example.com",
        password="OldPass123",
        mode=LoginMode.JSON,
    )

    response = await client.post(
        f"{USERS_API}/change-password",
        headers=auth_headers(token),
        json={"old_password": "WrongOld123", "new_password": "NewPass123"},
    )

    assert response.status_code == 400
    assert_detail_payload(response.json())

    async with db_session_factory() as session:
        unchanged_user = await session.get(User, user.id)
        assert unchanged_user is not None
        assert verify_password("OldPass123", unchanged_user.password_hash)


@pytest.mark.asyncio
async def test_request_password_reset(client, create_user, sent_emails):
    await create_user(email="member@example.com", password="UserPass123")

    response = await client.post(
        f"{USERS_API}/request-password-reset",
        json={"email": "member@example.com"},
    )

    assert response.status_code == 200
    assert_detail_payload(response.json())
    assert len(sent_emails) == 1
    assert sent_emails[0]["to"] == "member@example.com"
    assert "token=" in sent_emails[0]["body"]


@pytest.mark.asyncio
async def test_reset_password(client, create_user, db_session_factory):
    user = await create_user(email="member@example.com", password="UserPass123")
    token = create_reset_token(user.id)

    response = await client.post(
        f"{USERS_API}/reset-password",
        json={"token": token, "new_password": "ResetPass123"},
    )

    assert response.status_code == 200
    assert_detail_payload(response.json())

    async with db_session_factory() as session:
        updated_user = await session.get(User, user.id)
        assert updated_user is not None
        assert verify_password("ResetPass123", updated_user.password_hash)


@pytest.mark.asyncio
async def test_reset_password_rejects_invalid_token(client):
    response = await client.post(
        f"{USERS_API}/reset-password",
        json={"token": "not-a-valid-token", "new_password": "ResetPass123"},
    )

    assert response.status_code == 400
    assert_detail_payload(response.json())


@pytest.mark.asyncio
async def test_admin_change_password(client, create_user, login, db_session_factory):
    await create_user(
        email="root@example.com",
        password="RootPass123",
        role=UserRole.SUPERADMIN,
    )
    target = await create_user(email="member@example.com", password="UserPass123")
    token = await login(email="root@example.com", password="RootPass123")

    response = await client.post(
        f"{USERS_API}/users/{target.id}/change-password",
        headers=auth_headers(token),
        json={"new_password": "ChangedByAdmin123"},
    )

    assert response.status_code == 200
    assert_detail_payload(response.json())

    async with db_session_factory() as session:
        updated_user = await session.get(User, target.id)
        assert updated_user is not None
        assert verify_password("ChangedByAdmin123", updated_user.password_hash)
