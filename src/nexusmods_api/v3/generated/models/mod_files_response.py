"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFilesResponse(NexusModel):
    """Models the ModFilesResponse schema from the pinned Nexus Mods REST v3..."""

    mod_files: list[JsonValue]
    """The embedded ModFileWithAggregates data for this ModFilesResponse value."""
