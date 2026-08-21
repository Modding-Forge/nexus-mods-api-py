"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersionDependenciesResponse(NexusModel):
    """Models the ModFileVersionDependenciesResponse REST v3 schema.

    Models the ModFileVersionDependenciesResponse schema from the pinned Nexus Mods REST\
 v3 OpenAPI document.
    """

    dependency_definitions: list[JsonValue]
    """Raw (non-materialized) mod-file version-range dependency definitions, as authored\
. These are the stored min/max version bounds, not the resolved candidate versions. Use \
the materialized endpoint to resolve them.
    """

    dlc_dependency_definitions: list[JsonValue]
    """DLC dependency definitions.
    """
