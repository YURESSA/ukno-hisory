USERS_API = "/api/v1/users"
AUTH_API = "/api/v1/auth"


def auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def assert_token_payload(payload: dict) -> None:
    assert "access_token" in payload
    assert "token_type" in payload
    assert payload["token_type"] == "bearer"
    assert isinstance(payload["access_token"], str)
    assert payload["access_token"]


def assert_user_payload(payload: dict, *, email: str, role: str) -> None:
    assert "id" in payload
    assert "email" in payload
    assert "role" in payload
    assert isinstance(payload["id"], int)
    assert payload["email"] == email
    assert payload["role"] == role


def assert_detail_payload(payload: dict) -> None:
    assert "detail" in payload
    assert isinstance(payload["detail"], str)
    assert payload["detail"]
