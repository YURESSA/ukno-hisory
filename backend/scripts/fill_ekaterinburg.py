"""Однократное добавление проверенных материалов через административный API."""

import argparse
import getpass
import json
import os
from pathlib import Path
from urllib.parse import quote

import httpx

CONTENT_DIR = Path(__file__).resolve().parents[2] / "content" / "ekaterinburg"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://localhost:8000")
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    email = os.getenv("CONTENT_ADMIN_EMAIL") or input("Email администратора: ")
    password = os.getenv("CONTENT_ADMIN_PASSWORD") or getpass.getpass("Пароль: ")
    content = json.loads((CONTENT_DIR / "content.json").read_text(encoding="utf-8-sig"))
    report = {"base_url": args.base_url, "created": [], "updated": []}

    def record(group, entry):
        report[group].append(entry)
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def image(name):
        return (name, (CONTENT_DIR / "images" / name).read_bytes(), "image/png")

    with httpx.Client(
        base_url=args.base_url.rstrip("/") + "/api/v1/", timeout=90
    ) as client:

        def api(method, path, **kwargs):
            response = client.request(method, path, **kwargs)
            if response.is_error:
                raise RuntimeError(
                    f"{method} {path}: {response.status_code} {response.text[:500]}"
                )
            return response.json()

        token = api("POST", "users/login", json={"email": email, "password": password})
        client.headers["Authorization"] = "Bearer " + token["access_token"]
        existing_timeline = api("GET", "timeline")
        for item in content["timeline"]:
            if any(
                old["year"] == item["year"] and old["text"] == item["text"]
                for old in existing_timeline
            ):
                continue
            created = api(
                "POST",
                "timeline",
                data={"year": str(item["year"]), "text": item["text"]},
                files={"image": image(item["image"])},
            )
            record("created", {"type": "timeline", "id": created["id"]})

        existing_enterprises = api("GET", "enterprise-history/admin")
        for item in content["enterprises"]:
            if any(old["title"] == item["title"] for old in existing_enterprises):
                continue
            fields = {
                key: item[key]
                for key in (
                    "title",
                    "subdistrict",
                    "general_subtitle",
                    "detail_subtitle",
                    "short_description",
                )
            }
            fields["is_draft"] = "true"
            created = api(
                "POST",
                "enterprise-history",
                data=fields,
                files={
                    "general_main_image": image(item["image"]),
                    "detail_main_image": image(item["image"]),
                },
            )
            item_id = created["id"]
            record("created", {"type": "enterprise-history", "id": item_id})
            for position, text in enumerate(item["slides"]):
                api(
                    "POST",
                    f"enterprise-history/{item_id}/how-it-was",
                    data={"text": text, "order_index": str(position)},
                )
            api("PATCH", f"enterprise-history/{item_id}", json={"is_draft": False})

        for item in content["subdistricts"]:
            path = "subdistricts/" + quote(item["name"], safe="")
            existing = api("GET", path)
            if not existing["description"]:
                api("PATCH", path, json={"description": item["description"]})
                record("updated", {"type": "subdistrict", "name": item["name"]})
            if not existing["image"]:
                api("PUT", path + "/image", files={"image": image(item["image"])})

        existing_quiz = api("GET", "quiz")
        for item in content["quiz"]:
            if any(old["question"] == item["question"] for old in existing_quiz):
                continue
            created = api(
                "POST",
                "quiz",
                json={
                    "question": item["question"],
                    "explanation": item["explanation"],
                    "options": [
                        {"text": text, "is_correct": index == item["correct"]}
                        for index, text in enumerate(item["answers"])
                    ],
                },
            )
            record("created", {"type": "quiz", "id": created["id"]})
    print(f"Создано записей: {len(report['created'])}")
    print(f"Обновлено описаний подрайонов: {len(report['updated'])}")
    print(f"Отчёт: {args.report}")


if __name__ == "__main__":
    main()
