import pytest

from app.modules.users.models import UserRole
from tests.users.helpers import USERS_API, auth_headers


@pytest.mark.asyncio
async def test_profile_uses_current_database_role(client, create_user, login):
    user = await create_user(email="editor@example.com", password="AdminPass123")
    token = await login(email=user.email, password="AdminPass123")
    response = await client.get(f"{USERS_API}/me", headers=auth_headers(token))
    assert response.status_code == 200
    assert response.json() == {"id": user.id, "email": user.email, "role": "admin"}


@pytest.mark.asyncio
@pytest.mark.parametrize("authenticated", [False, True])
async def test_only_superadmin_can_edit_users(
    client, create_user, login, authenticated
):
    admin = await create_user(email="admin@example.com", password="AdminPass123")
    headers = {}
    if authenticated:
        token = await login(email=admin.email, password="AdminPass123")
        headers = auth_headers(token)
    response = await client.patch(
        f"{USERS_API}/users/{admin.id}",
        headers=headers,
        json={"role": "superadmin"},
    )
    assert response.status_code == (403 if authenticated else 401)


@pytest.mark.asyncio
async def test_superadmin_edits_email_and_role_and_demotes_existing_token(
    client, create_user, login
):
    root = await create_user(
        email="root@example.com", password="RootPass123", role=UserRole.SUPERADMIN
    )
    target = await create_user(email="target@example.com", password="AdminPass123")
    root_headers = auth_headers(await login(email=root.email, password="RootPass123"))
    response = await client.patch(
        f"{USERS_API}/users/{target.id}",
        headers=root_headers,
        json={"email": "updated@example.com", "role": "superadmin"},
    )
    assert response.status_code == 200
    assert response.json()["role"] == "superadmin"
    token = await login(email="updated@example.com", password="AdminPass123")
    response = await client.patch(
        f"{USERS_API}/users/{target.id}", headers=root_headers, json={"role": "admin"}
    )
    assert response.status_code == 200
    response = await client.patch(
        f"{USERS_API}/users/{root.id}",
        headers=auth_headers(token),
        json={"role": "admin"},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "body,expected",
    [
        ({"role": "admin"}, 400),
        ({"role": "unknown"}, 422),
        ({"email": None}, 422),
        ({}, 422),
    ],
)
async def test_editor_rejects_invalid_changes(
    client, create_user, login, body, expected
):
    root = await create_user(
        email="root@example.com", password="RootPass123", role=UserRole.SUPERADMIN
    )
    headers = auth_headers(await login(email=root.email, password="RootPass123"))
    response = await client.patch(
        f"{USERS_API}/users/{root.id}", headers=headers, json=body
    )
    assert response.status_code == expected
    response = await client.get(f"{USERS_API}/me", headers=headers)
    assert response.json()["role"] == "superadmin"


@pytest.mark.asyncio
async def test_editor_duplicate_email_and_missing_user(client, create_user, login):
    root = await create_user(
        email="root@example.com", password="RootPass123", role=UserRole.SUPERADMIN
    )
    target = await create_user(email="target@example.com", password="AdminPass123")
    headers = auth_headers(await login(email=root.email, password="RootPass123"))
    response = await client.patch(
        f"{USERS_API}/users/{target.id}", headers=headers, json={"email": root.email}
    )
    assert response.status_code == 409
    response = await client.patch(
        f"{USERS_API}/users/99999", headers=headers, json={"role": "admin"}
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_password_minimum_length(client, create_user, login):
    user = await create_user(email="admin@example.com", password="AdminPass123")
    headers = auth_headers(await login(email=user.email, password="AdminPass123"))
    response = await client.post(
        f"{USERS_API}/change-password",
        headers=headers,
        json={"old_password": "AdminPass123", "new_password": "short"},
    )
    assert response.status_code == 422
