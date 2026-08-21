"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class UpdateModFileVersionDlcDependenciesRequest(NexusModel):
    """Models the UpdateModFileVersionDlcDependenciesRequest REST v3 schema.

    Models the UpdateModFileVersionDlcDependenciesRequest schema from the pinned Nexus M\
ods REST v3 OpenAPI document.
    """

    dlc_dependency_definitions: list[JsonValue]
    """The full set of DLC dependency definitions for the version. Replaces any
    existing definitions. An empty array clears all DLC dependencies.
    """
