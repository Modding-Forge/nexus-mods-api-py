"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersionDependencyRangesMaterializedResponse(NexusModel):
    """Models the ModFileVersionDependencyRangesMaterializedResponse schema..."""

    dependencies: list[JsonValue]
    """Materialized version-range dependencies (each stored range resolved..."""
