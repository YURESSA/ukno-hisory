PROJECTS_API = "/api/v1/student-projects"
PUBLIC_SUMMARY_KEYS = {
    "id",
    "title",
    "author",
    "short_description",
    "main_image",
}
PUBLIC_DETAIL_KEYS = {"id", "title", "main_image", "description", "tags", "gallery"}
PUBLIC_TAG_KEYS = {"author", "year", "tag_one", "tag_two"}
ADMIN_SUMMARY_KEYS = {
    "id",
    "title",
    "author",
    "short_description",
    "main_image",
    "is_draft",
}
ADMIN_DETAIL_KEYS = {
    "id",
    "title",
    "author",
    "short_description",
    "description",
    "main_image",
    "year",
    "tag_one",
    "tag_two",
    "is_draft",
    "gallery",
}
GALLERY_ITEM_KEYS = {"id", "image", "position"}


def build_image_file(
    name: str,
    content: bytes = b"fake-image-content",
    content_type: str = "image/jpeg",
) -> tuple[str, bytes, str]:
    return (name, content, content_type)


def assert_student_project_gallery_item(payload: dict) -> None:
    assert set(payload) == GALLERY_ITEM_KEYS
    assert isinstance(payload["id"], int)
    assert isinstance(payload["image"], str)
    assert isinstance(payload["position"], int)


def assert_student_project_public_summary(payload: dict) -> None:
    assert set(payload) == PUBLIC_SUMMARY_KEYS
    assert isinstance(payload["id"], int)
    assert isinstance(payload["title"], str)
    assert isinstance(payload["author"], str)
    assert isinstance(payload["short_description"], str)
    assert isinstance(payload["main_image"], str)


def assert_student_project_public_detail(payload: dict) -> None:
    assert set(payload) == PUBLIC_DETAIL_KEYS
    assert isinstance(payload["id"], int)
    assert isinstance(payload["title"], str)
    assert isinstance(payload["main_image"], str)
    assert isinstance(payload["description"], str)
    assert set(payload["tags"]) == PUBLIC_TAG_KEYS
    assert isinstance(payload["tags"]["author"], str)
    assert isinstance(payload["tags"]["year"], int)
    assert payload["tags"]["tag_one"] is None or isinstance(
        payload["tags"]["tag_one"], str
    )
    assert payload["tags"]["tag_two"] is None or isinstance(
        payload["tags"]["tag_two"], str
    )
    assert isinstance(payload["gallery"], list)
    for item in payload["gallery"]:
        assert_student_project_gallery_item(item)


def assert_student_project_admin_summary(payload: dict) -> None:
    assert set(payload) == ADMIN_SUMMARY_KEYS
    assert isinstance(payload["id"], int)
    assert payload["title"] is None or isinstance(payload["title"], str)
    assert payload["author"] is None or isinstance(payload["author"], str)
    assert payload["short_description"] is None or isinstance(
        payload["short_description"], str
    )
    assert payload["main_image"] is None or isinstance(payload["main_image"], str)
    assert isinstance(payload["is_draft"], bool)


def assert_student_project_admin_detail(payload: dict) -> None:
    assert set(payload) == ADMIN_DETAIL_KEYS
    assert isinstance(payload["id"], int)
    assert payload["title"] is None or isinstance(payload["title"], str)
    assert payload["author"] is None or isinstance(payload["author"], str)
    assert payload["short_description"] is None or isinstance(
        payload["short_description"], str
    )
    assert payload["description"] is None or isinstance(payload["description"], str)
    assert payload["main_image"] is None or isinstance(payload["main_image"], str)
    assert payload["year"] is None or isinstance(payload["year"], int)
    assert payload["tag_one"] is None or isinstance(payload["tag_one"], str)
    assert payload["tag_two"] is None or isinstance(payload["tag_two"], str)
    assert isinstance(payload["is_draft"], bool)
    assert isinstance(payload["gallery"], list)
    for item in payload["gallery"]:
        assert_student_project_gallery_item(item)
