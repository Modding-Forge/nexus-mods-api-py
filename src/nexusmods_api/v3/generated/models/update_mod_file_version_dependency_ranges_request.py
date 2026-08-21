"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class UpdateModFileVersionDependencyRangesRequest(NexusModel):
    """Models the UpdateModFileVersionDependencyRangesRequest REST v3 schema.

    Models the UpdateModFileVersionDependencyRangesRequest schema from the pinned Nexus \
Mods REST v3 OpenAPI document.
    """

    dependency_definitions: list[JsonValue]
    """The embedded ModFileVersionDependencyRangeDefinitionInput data for this UpdateMod\
FileVersionDependencyRangesRequest value.
    """
