"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersionsBatchResponse(NexusModel):
    """Models the ModFileVersionsBatchResponse REST v3 schema.

    Models the ModFileVersionsBatchResponse schema from the pinned Nexus Mods REST v3 Op\
enAPI document.
    """

    versions: list[JsonValue]
    """The embedded ModFileVersionDetail data for this ModFileVersionsBatchResponse valu\
e.
    """
