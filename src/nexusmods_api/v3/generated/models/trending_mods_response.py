"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class TrendingModsResponse(NexusModel):
    """Models the TrendingModsResponse REST v3 schema.

    Models the TrendingModsResponse schema from the pinned Nexus Mods REST v3 OpenAPI do\
cument.
    """

    mods: list[JsonValue]
    """The embedded TrendingMod data for this TrendingModsResponse value.
    """
