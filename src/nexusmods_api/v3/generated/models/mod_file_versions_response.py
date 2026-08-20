"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersionsResponse(NexusModel):
    """Models the ModFileVersionsResponse schema from the pinned Nexus Mods..."""

    versions: list[JsonValue]
    """The embedded ModFileVersion data for this ModFileVersionsResponse value."""
