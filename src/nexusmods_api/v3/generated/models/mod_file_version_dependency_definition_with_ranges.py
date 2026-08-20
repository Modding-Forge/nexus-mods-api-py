"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersionDependencyDefinitionWithRanges(NexusModel):
    """Models the ModFileVersionDependencyDefinitionWithRanges schema from..."""

    id: str
    """The unique identifier for the dependency definition."""

    ranges: list[JsonValue]
    """The embedded ModFileVersionDependencyRange data for this..."""
