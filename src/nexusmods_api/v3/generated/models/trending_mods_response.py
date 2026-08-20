"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class TrendingModsResponse(NexusModel):
    """Models the TrendingModsResponse schema from the pinned Nexus Mods..."""

    mods: list[JsonValue]
    """The embedded TrendingMod data for this TrendingModsResponse value."""
