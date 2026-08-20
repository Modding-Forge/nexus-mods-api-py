"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersionDependencyRangesResponse(NexusModel):
    """Models the ModFileVersionDependencyRangesResponse schema from the..."""

    dependency_definitions: list[JsonValue]
    """The embedded ModFileVersionDependencyDefinitionWithRanges data for..."""
