import enum

import pytest

from tests.users.helpers import AUTH_API, USERS_API, assert_token_payload


class LoginMode(str, enum.Enum):
    JSON = "json"
    FORM = "form"


@pytest.fixture
def login(client):
    async def _login(
        *, email: str, password: str, mode: LoginMode = LoginMode.FORM
    ) -> str:
        if mode == LoginMode.JSON:
            response = await client.post(
                f"{USERS_API}/login",
                json={"email": email, "password": password},
            )
        else:
            response = await client.post(
                f"{AUTH_API}/login",
                data={"username": email, "password": password},
            )

        assert response.status_code == 200
        payload = response.json()
        assert_token_payload(payload)
        return payload["access_token"]

    return _login
