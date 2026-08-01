"""Copyright (c) Modding Forge."""

from nexusmods_api.types import JsonValue


def mod_payload() -> dict[str, JsonValue]:
    """Returns minimal valid mod metadata.

    Returns:
        dict[str, JsonValue]: Test mod payload.
    """

    return {
        "mod_id": 2,
        "game_id": 1,
        "domain_name": "game",
        "category_id": 3,
        "contains_adult_content": False,
        "name": "Test Mod",
    }


def file_payload() -> dict[str, JsonValue]:
    """Returns minimal valid file metadata.

    Returns:
        dict[str, JsonValue]: Test file payload.
    """

    return {
        "file_id": 4,
        "category_id": 1,
        "category_name": "MAIN",
        "name": "Main File",
    }


def response_payload(method: str, path: str) -> JsonValue:
    """Returns a valid response for every hand-written v1 route.

    Args:
        method (str): HTTP request method.
        path (str): Request URL path.

    Returns:
        JsonValue: Route-specific response payload.
    """

    if path.endswith("/users/validate"):
        return {
            "user_id": 1,
            "key": "masked-by-model-repr",
            "name": "User",
            "is_premium": True,
            "is_supporter": False,
            "email": "user@example.com",
        }
    if path.endswith("/user/tracked_mods"):
        if method == "GET":
            return [{"mod_id": 2, "domain_name": "game"}]
        return {"message": "tracking updated"}
    if path.endswith("/user/endorsements"):
        return [
            {
                "mod_id": 2,
                "domain_name": "game",
                "date": 1,
                "status": "Endorsed",
            }
        ]
    if path.endswith("/colourschemes"):
        return [
            {
                "id": 1,
                "name": "Dark",
                "primary_colour": "#000",
                "secondary_colour": "#111",
                "darker_colour": "#222",
            }
        ]
    if path.endswith("/games"):
        return [{"id": 1, "domain_name": "game", "name": "Game"}]
    if path.endswith("/games/game"):
        return {
            "id": 1,
            "domain_name": "game",
            "name": "Game",
            "categories": [
                {"category_id": 3, "name": "Category", "parent_category": False}
            ],
        }
    if path.endswith(("/latest_added", "/latest_updated", "/trending")):
        return [mod_payload()]
    if path.endswith("/mods/updated"):
        return [
            {
                "mod_id": 2,
                "latest_file_update": 10,
                "latest_mod_activity": 11,
            }
        ]
    if path.endswith("/changelogs"):
        return {"1.0": ["Initial release"]}
    if path.endswith("/files/4/download_link"):
        return [
            {
                "URI": "https://download.example/file",
                "name": "CDN",
                "short_name": "cdn",
            }
        ]
    if path.endswith("/files/4"):
        return file_payload()
    if path.endswith("/files"):
        return {
            "files": [file_payload()],
            "file_updates": [
                {
                    "new_file_id": 4,
                    "new_file_name": "New",
                    "old_file_id": 3,
                    "old_file_name": "Old",
                }
            ],
        }
    if "/md5_search/" in path:
        return [{"mod": mod_payload(), "file_details": file_payload()}]
    if path.endswith(("/endorse", "/abstain")):
        return {"message": "endorsement updated", "status": "Endorsed"}
    if path.endswith("/mods/2"):
        return mod_payload()
    raise AssertionError(f"Unexpected route: {method} {path}")
