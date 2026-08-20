"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersionDlcDependenciesResponse(NexusModel):
    """Models the ModFileVersionDlcDependenciesResponse schema from the..."""

    dlc_dependency_definitions: list[JsonValue]
    """DLC dependency definitions."""
