from datetime import datetime, timedelta, timezone

import pytest
from jose import jwt

from app.core.config import settings
from app.core.security import ALGORITHM


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "case",
    ["expired", "wrong_signature", "malformed", "missing_subject", "bad_subject"],
)
async def test_invalid_access_token_returns_401(client, case):
    payload = {
        "sub": "1",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
    }
    key = settings.SECRET_KEY
    if case == "expired":
        payload["exp"] = datetime.now(timezone.utc) - timedelta(minutes=1)
    elif case == "wrong_signature":
        key += "-wrong-key"
    elif case == "missing_subject":
        payload.pop("sub")
    elif case == "bad_subject":
        payload["sub"] = "not-a-user-id"

    token = (
        "invalid-token" if case == "malformed" else jwt.encode(payload, key, ALGORITHM)
    )
    response = await client.get(
        "/api/v1/student-projects/admin",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"
    assert "detail" in response.json()
