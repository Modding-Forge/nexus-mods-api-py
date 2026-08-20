"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModsBatchResponse(NexusModel):
    """Models the ModsBatchResponse schema from the pinned Nexus Mods REST..."""

    mods: list[JsonValue]
    """The embedded ModDetail data for this ModsBatchResponse value."""
