"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class MoveModFileVersionsRequest(NexusModel):
    """Models the MoveModFileVersionsRequest REST v3 schema.

    Models the MoveModFileVersionsRequest schema from the pinned Nexus Mods REST v3 Open\
API document.
    """

    target: JsonValue
    """The embedded MoveToPosition data for this MoveModFileVersionsRequest value.
    """

    version_ids: list[str]
    """The unique identifiers for the mod file versions to move.
    Versions are inserted in this order, and `version_ids` is expected to be ordered fro\
m earliest to latest version.
    """
