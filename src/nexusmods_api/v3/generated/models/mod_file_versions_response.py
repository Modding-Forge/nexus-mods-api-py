"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersionsResponse(NexusModel):
    """Models the ModFileVersionsResponse REST v3 schema.

    Models the ModFileVersionsResponse schema from the pinned Nexus Mods REST v3 OpenAPI\
 document.
    """

    versions: list[JsonValue]
    """The embedded ModFileVersion data for this ModFileVersionsResponse value.
    """
