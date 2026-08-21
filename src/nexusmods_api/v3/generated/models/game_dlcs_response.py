"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class GameDlcsResponse(NexusModel):
    """Models the GameDlcsResponse REST v3 schema.

    Models the GameDlcsResponse schema from the pinned Nexus Mods REST v3 OpenAPI docume\
nt.
    """

    dlcs: list[JsonValue]
    """The embedded Dlc data for this GameDlcsResponse value.
    """
