"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersionDlcDependenciesResponse(NexusModel):
    """Models the ModFileVersionDlcDependenciesResponse REST v3 schema.

    Models the ModFileVersionDlcDependenciesResponse schema from the pinned Nexus Mods R\
EST v3 OpenAPI document.
    """

    dlc_dependency_definitions: list[JsonValue]
    """DLC dependency definitions.
    """
