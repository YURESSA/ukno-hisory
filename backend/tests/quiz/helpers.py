QUIZ_API = "/api/v1/quiz"
QUIZ_KEYS = {"id", "question", "explanation", "image", "options"}
QUIZ_OPTION_KEYS = {"id", "text", "is_correct", "position"}


def build_image_file(
    name: str,
    content: bytes = b"fake-image-content",
    content_type: str = "image/jpeg",
) -> dict:
    return {"image": (name, content, content_type)}


def assert_quiz_option_payload(
    payload: dict,
    *,
    text: str,
    is_correct: bool,
    position: int,
) -> None:
    assert set(payload) == QUIZ_OPTION_KEYS
    assert isinstance(payload["id"], int)
    assert payload["text"] == text
    assert isinstance(payload["text"], str)
    assert payload["is_correct"] is is_correct
    assert isinstance(payload["is_correct"], bool)
    assert payload["position"] == position
    assert isinstance(payload["position"], int)


def assert_quiz_payload(
    payload: dict,
    *,
    question: str,
    explanation: str | None,
    image: str | None,
    options: list[dict],
) -> None:
    assert set(payload) == QUIZ_KEYS
    assert isinstance(payload["id"], int)
    assert payload["question"] == question
    assert payload["explanation"] == explanation
    assert payload["image"] == image
    assert isinstance(payload["options"], list)
    assert len(payload["options"]) == len(options)
    for index, option in enumerate(payload["options"]):
        expected = options[index]
        assert_quiz_option_payload(
            option,
            text=expected["text"],
            is_correct=expected["is_correct"],
            position=index,
        )
