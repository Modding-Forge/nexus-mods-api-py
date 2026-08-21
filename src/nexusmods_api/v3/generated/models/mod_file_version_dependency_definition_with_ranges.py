"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersionDependencyDefinitionWithRanges(NexusModel):
    """Models the ModFileVersionDependencyDefinitionWithRanges REST v3 schema.

    Models the ModFileVersionDependencyDefinitionWithRanges schema from the pinned Nexus\
 Mods REST v3 OpenAPI document.
    """

    id: str
    """The unique identifier for the dependency definition.
    """

    ranges: list[JsonValue]
    """The embedded ModFileVersionDependencyRange data for this ModFileVersionDependency\
DefinitionWithRanges value.
    """
