ENTERPRISE_HISTORY_API = "/api/v1/enterprise-history"
PUBLIC_SUMMARY_KEYS = {
    "id",
    "title",
    "subtitle",
    "short_description",
    "main_image",
}
PUBLIC_DETAIL_KEYS = {
    "id",
    "title",
    "subtitle",
    "short_description",
    "main_image",
    "how_it_was",
    "gallery",
}
ADMIN_SUMMARY_KEYS = {
    "id",
    "title",
    "general_subtitle",
    "short_description",
    "general_main_image",
    "is_draft",
}
ADMIN_DETAIL_KEYS = {
    "id",
    "title",
    "general_subtitle",
    "detail_subtitle",
    "short_description",
    "general_main_image",
    "detail_main_image",
    "is_draft",
    "how_it_was",
    "gallery",
}
SLIDE_ITEM_KEYS = {"id", "text", "image", "order_index"}
GALLERY_ITEM_KEYS = {"id", "image", "position"}


def build_image_file(
    name: str,
    content: bytes = b"fake-image-content",
    content_type: str = "image/jpeg",
) -> tuple[str, bytes, str]:
    return (name, content, content_type)


def assert_enterprise_history_slide_item(payload: dict) -> None:
    assert set(payload) == SLIDE_ITEM_KEYS
    assert isinstance(payload["id"], int)
    assert payload["text"] is None or isinstance(payload["text"], str)
    assert payload["image"] is None or isinstance(payload["image"], str)
    assert isinstance(payload["order_index"], int)


def assert_enterprise_history_gallery_item(payload: dict) -> None:
    assert set(payload) == GALLERY_ITEM_KEYS
    assert isinstance(payload["id"], int)
    assert isinstance(payload["image"], str)
    assert isinstance(payload["position"], int)


def assert_enterprise_history_public_summary(payload: dict) -> None:
    assert set(payload) == PUBLIC_SUMMARY_KEYS
    assert isinstance(payload["id"], int)
    assert isinstance(payload["title"], str)
    assert isinstance(payload["subtitle"], str)
    assert isinstance(payload["short_description"], str)
    assert isinstance(payload["main_image"], str)


def assert_enterprise_history_public_detail(payload: dict) -> None:
    assert set(payload) == PUBLIC_DETAIL_KEYS
    assert isinstance(payload["id"], int)
    assert isinstance(payload["title"], str)
    assert isinstance(payload["subtitle"], str)
    assert isinstance(payload["short_description"], str)
    assert isinstance(payload["main_image"], str)
    assert isinstance(payload["how_it_was"], list)
    for item in payload["how_it_was"]:
        assert_enterprise_history_slide_item(item)
    assert isinstance(payload["gallery"], list)
    for item in payload["gallery"]:
        assert_enterprise_history_gallery_item(item)


def assert_enterprise_history_admin_summary(payload: dict) -> None:
    assert set(payload) == ADMIN_SUMMARY_KEYS
    assert isinstance(payload["id"], int)
    assert payload["title"] is None or isinstance(payload["title"], str)
    assert payload["general_subtitle"] is None or isinstance(
        payload["general_subtitle"], str
    )
    assert payload["short_description"] is None or isinstance(
        payload["short_description"], str
    )
    assert payload["general_main_image"] is None or isinstance(
        payload["general_main_image"], str
    )
    assert isinstance(payload["is_draft"], bool)


def assert_enterprise_history_admin_detail(payload: dict) -> None:
    assert set(payload) == ADMIN_DETAIL_KEYS
    assert isinstance(payload["id"], int)
    assert payload["title"] is None or isinstance(payload["title"], str)
    assert payload["general_subtitle"] is None or isinstance(
        payload["general_subtitle"], str
    )
    assert payload["detail_subtitle"] is None or isinstance(
        payload["detail_subtitle"], str
    )
    assert payload["short_description"] is None or isinstance(
        payload["short_description"], str
    )
    assert payload["general_main_image"] is None or isinstance(
        payload["general_main_image"], str
    )
    assert payload["detail_main_image"] is None or isinstance(
        payload["detail_main_image"], str
    )
    assert isinstance(payload["is_draft"], bool)
    assert isinstance(payload["how_it_was"], list)
    for item in payload["how_it_was"]:
        assert_enterprise_history_slide_item(item)
    assert isinstance(payload["gallery"], list)
    for item in payload["gallery"]:
        assert_enterprise_history_gallery_item(item)
