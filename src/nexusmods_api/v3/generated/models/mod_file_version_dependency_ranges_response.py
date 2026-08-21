"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersionDependencyRangesResponse(NexusModel):
    """Models the ModFileVersionDependencyRangesResponse REST v3 schema.

    Models the ModFileVersionDependencyRangesResponse schema from the pinned Nexus Mods \
REST v3 OpenAPI document.
    """

    dependency_definitions: list[JsonValue]
    """The embedded ModFileVersionDependencyDefinitionWithRanges data for this ModFileVe\
rsionDependencyRangesResponse value.
    """
