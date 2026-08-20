"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class GameDlcsResponse(NexusModel):
    """Models the GameDlcsResponse schema from the pinned Nexus Mods REST v3..."""

    dlcs: list[JsonValue]
    """The embedded Dlc data for this GameDlcsResponse value."""
