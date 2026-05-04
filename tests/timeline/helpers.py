TIMELINE_API = "/api/v1/timeline"


def assert_timeline_payload(
    payload: dict,
    *,
    year: int,
    image: str,
    text: str,
) -> None:
    assert "id" in payload
    assert isinstance(payload["id"], int)
    assert payload["year"] == year
    assert payload["image"] == image
    assert payload["text"] == text
