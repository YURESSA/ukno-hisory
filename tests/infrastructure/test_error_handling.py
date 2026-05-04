import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.modules.timeline.router import get_service
from tests.timeline.helpers import TIMELINE_API
from tests.users.helpers import assert_detail_payload


@pytest.mark.asyncio
async def test_validation_errors_are_returned_in_russian(client):
    response = await client.get(f"{TIMELINE_API}/invalid-id")

    assert response.status_code == 422
    payload = response.json()
    assert payload["detail"] == "Ошибка валидации запроса"
    assert "errors" in payload
    assert isinstance(payload["errors"], list)


@pytest.mark.asyncio
async def test_unhandled_errors_return_safe_russian_message(client):
    class BrokenTimelineService:
        async def get_entries(self):
            raise RuntimeError("boom")

    app.dependency_overrides[get_service] = lambda: BrokenTimelineService()
    try:
        transport = ASGITransport(app=app, raise_app_exceptions=False)
        async with AsyncClient(
            transport=transport, base_url="http://test"
        ) as safe_client:
            response = await safe_client.get(TIMELINE_API)
    finally:
        app.dependency_overrides.pop(get_service, None)

    assert response.status_code == 500
    assert_detail_payload(response.json())
    assert response.json()["detail"] == "Внутренняя ошибка сервера"
