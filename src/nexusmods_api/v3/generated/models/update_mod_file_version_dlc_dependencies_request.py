"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class UpdateModFileVersionDlcDependenciesRequest(NexusModel):
    """Models the UpdateModFileVersionDlcDependenciesRequest schema from the..."""

    dlc_dependency_definitions: list[JsonValue]
    """The full set of DLC dependency definitions for the version. Replaces..."""
