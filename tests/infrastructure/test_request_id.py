import pytest

from tests.timeline.helpers import TIMELINE_API


@pytest.mark.asyncio
async def test_response_contains_generated_request_id(client):
    response = await client.get(TIMELINE_API)

    assert response.status_code == 200
    assert "X-Request-ID" in response.headers
    assert response.headers["X-Request-ID"]


@pytest.mark.asyncio
async def test_response_preserves_incoming_request_id(client):
    response = await client.get(
        TIMELINE_API,
        headers={"X-Request-ID": "test-request-id"},
    )

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "test-request-id"
