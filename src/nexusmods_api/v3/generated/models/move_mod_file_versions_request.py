"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class MoveModFileVersionsRequest(NexusModel):
    """Models the MoveModFileVersionsRequest schema from the pinned Nexus..."""

    target: JsonValue
    """The embedded MoveToPosition data for this MoveModFileVersionsRequest..."""

    version_ids: list[str]
    """The unique identifiers for the mod file versions to move. Versions..."""
