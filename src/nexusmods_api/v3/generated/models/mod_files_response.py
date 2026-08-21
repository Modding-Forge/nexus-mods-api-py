"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFilesResponse(NexusModel):
    """Models the ModFilesResponse REST v3 schema.

    Models the ModFilesResponse schema from the pinned Nexus Mods REST v3 OpenAPI docume\
nt.
    """

    mod_files: list[JsonValue]
    """The embedded ModFileWithAggregates data for this ModFilesResponse value.
    """
