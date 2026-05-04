TIMELINE_API = "/api/v1/timeline"
TIMELINE_RESPONSE_KEYS = {"id", "year", "image", "text"}


def assert_timeline_payload(
    payload: dict,
    *,
    year: int,
    image: str,
    text: str,
) -> None:
    assert set(payload) == TIMELINE_RESPONSE_KEYS
    assert isinstance(payload["id"], int)
    assert payload["year"] == year
    assert isinstance(payload["year"], int)
    assert payload["image"] == image
    assert isinstance(payload["image"], str)
    assert payload["text"] == text
    assert isinstance(payload["text"], str)
