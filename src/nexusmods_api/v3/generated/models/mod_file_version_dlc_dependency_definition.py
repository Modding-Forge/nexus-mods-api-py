"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersionDlcDependencyDefinition(NexusModel):
    """Models the ModFileVersionDlcDependencyDefinition schema from the..."""

    dlc_targets: list[JsonValue]
    """The DLCs that satisfy this definition (OR-alternatives)."""

    id: str
    """The unique identifier for the DLC dependency definition."""
