"""Copyright (c) Modding Forge."""

from nexusmods_api.types import JsonValue


def operation_payload(operation_name: str | None) -> dict[str, JsonValue]:
    """Returns valid data for every GraphQL convenience operation.

    Args:
        operation_name (str | None): Requested operation name.

    Returns:
        dict[str, JsonValue]: GraphQL response envelope.
    """

    pages: dict[str, JsonValue] = {
        "Games": {
            "games": {
                "nodes": [{"id": 1, "domainName": "game", "name": "Game"}],
                "totalCount": 1,
                "nodesCount": 1,
            }
        },
        "SearchMods": {
            "mods": {
                "nodes": [{"uid": "game:2", "modId": 2, "name": "Mod"}],
                "totalCount": 1,
            }
        },
        "ModFiles": {
            "modFiles": {
                "nodes": [{"uid": "game:2:4", "fileId": 4, "name": "File"}],
                "totalCount": 1,
            }
        },
    }
    values: dict[str, JsonValue] = {
        "Mod": {"mod": {"uid": "game:2", "modId": 2, "name": "Mod"}},
        "Collection": {
            "collection": {"id": 3, "slug": "collection", "name": "Collection"}
        },
        "Revision": {
            "collectionRevision": {"id": 5, "revisionNumber": 1}
        },
        "User": {"user": {"memberId": 6, "name": "User", "avatar": None}},
    }
    data: JsonValue = pages.get(operation_name or "")
    if data is None:
        data = values.get(operation_name or "", {"answer": 42})
    return {"data": data, "extensions": {"forwardCompatible": True}}
