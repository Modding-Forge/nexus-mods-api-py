"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersionDependencyRangesMaterializedResponse(NexusModel):
    """Models the ModFileVersionDependencyRangesMaterializedResponse REST v3 schema.

    Models the ModFileVersionDependencyRangesMaterializedResponse schema from the pinned\
 Nexus Mods REST v3 OpenAPI document.
    """

    dependencies: list[JsonValue]
    """Materialized version-range dependencies (each stored range resolved to its candid\
ate versions).
    """
