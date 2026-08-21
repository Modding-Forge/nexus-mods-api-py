"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModsBatchResponse(NexusModel):
    """Models the ModsBatchResponse REST v3 schema.

    Models the ModsBatchResponse schema from the pinned Nexus Mods REST v3 OpenAPI docum\
ent.
    """

    mods: list[JsonValue]
    """The embedded ModDetail data for this ModsBatchResponse value.
    """
