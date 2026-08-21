"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersionDependencyRangeDefinitionInput(NexusModel):
    """Models the ModFileVersionDependencyRangeDefinitionInput REST v3 schema.

    Models the ModFileVersionDependencyRangeDefinitionInput schema from the pinned Nexus\
 Mods REST v3 OpenAPI document.
    """

    ranges: list[JsonValue]
    """The embedded ModFileVersionDependencyRangeInput data for this ModFileVersionDepen\
dencyRangeDefinitionInput value.
    """
