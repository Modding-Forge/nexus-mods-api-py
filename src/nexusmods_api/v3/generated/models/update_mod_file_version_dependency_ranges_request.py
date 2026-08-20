"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class UpdateModFileVersionDependencyRangesRequest(NexusModel):
    """Models the UpdateModFileVersionDependencyRangesRequest schema from..."""

    dependency_definitions: list[JsonValue]
    """The embedded ModFileVersionDependencyRangeDefinitionInput data for..."""
