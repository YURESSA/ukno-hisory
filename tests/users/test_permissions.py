import pytest

from app.modules.users.models import UserRole
from tests.users.helpers import USERS_API, assert_detail_payload, auth_headers


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("method", "path_template", "body"),
    [
        ("get", f"{USERS_API}/users", None),
        ("get", f"{USERS_API}/users/{{target_id}}", None),
        ("delete", f"{USERS_API}/users/{{target_id}}", None),
        (
            "post",
            f"{USERS_API}/change-password",
            {"old_password": "OldPass123", "new_password": "NewPass123"},
        ),
        ("post", f"{USERS_API}/create-admin", {"email": "new-admin@example.com"}),
        (
            "post",
            f"{USERS_API}/users/{{target_id}}/change-password",
            {"new_password": "ChangedByAdmin123"},
        ),
        ("post", f"{USERS_API}/transfer-superadmin/{{target_id}}", None),
    ],
)
async def test_protected_user_endpoints_require_auth(
    client,
    create_user,
    method: str,
    path_template: str,
    body: dict | None,
):
    target = await create_user(email="member@example.com", password="UserPass123")
    path = path_template.format(target_id=target.id)
    request_kwargs = {"json": body} if body is not None else {}

    response = await getattr(client, method)(path, **request_kwargs)

    assert response.status_code == 401
    assert_detail_payload(response.json())


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("method", "path_template", "body"),
    [
        ("post", f"{USERS_API}/create-admin", {"email": "new-admin@example.com"}),
        (
            "post",
            f"{USERS_API}/users/{{target_id}}/change-password",
            {"new_password": "ChangedByAdmin123"},
        ),
        ("post", f"{USERS_API}/transfer-superadmin/{{target_id}}", None),
    ],
)
async def test_superadmin_endpoints_forbidden_for_admin(
    client,
    create_user,
    login,
    method: str,
    path_template: str,
    body: dict | None,
):
    await create_user(
        email="admin@example.com",
        password="AdminPass123",
        role=UserRole.ADMIN,
    )
    target = await create_user(email="member@example.com", password="UserPass123")
    token = await login(email="admin@example.com", password="AdminPass123")
    path = path_template.format(target_id=target.id)
    request_kwargs = {"json": body} if body is not None else {}

    response = await getattr(client, method)(
        path,
        headers=auth_headers(token),
        **request_kwargs,
    )

    assert response.status_code == 403
    assert_detail_payload(response.json())


@pytest.mark.asyncio
async def test_delete_user_returns_404_for_missing_user(client, create_user, login):
    await create_user(
        email="root@example.com",
        password="RootPass123",
        role=UserRole.SUPERADMIN,
    )
    token = await login(email="root@example.com", password="RootPass123")

    response = await client.delete(
        f"{USERS_API}/users/9999",
        headers=auth_headers(token),
    )

    assert response.status_code == 404
    assert_detail_payload(response.json())
