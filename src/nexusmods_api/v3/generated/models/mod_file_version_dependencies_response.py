"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersionDependenciesResponse(NexusModel):
    """Models the ModFileVersionDependenciesResponse schema from the pinned..."""

    dependency_definitions: list[JsonValue]
    """Raw (non-materialized) mod-file version-range dependency definitions,..."""

    dlc_dependency_definitions: list[JsonValue]
    """DLC dependency definitions."""
