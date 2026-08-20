"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersionDependencyRangeDefinitionInput(NexusModel):
    """Models the ModFileVersionDependencyRangeDefinitionInput schema from..."""

    ranges: list[JsonValue]
    """The embedded ModFileVersionDependencyRangeInput data for this..."""
