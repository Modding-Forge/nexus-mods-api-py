"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersionDlcDependencyDefinition(NexusModel):
    """Models the ModFileVersionDlcDependencyDefinition REST v3 schema.

    Models the ModFileVersionDlcDependencyDefinition schema from the pinned Nexus Mods R\
EST v3 OpenAPI document.
    """

    dlc_targets: list[JsonValue]
    """The DLCs that satisfy this definition (OR-alternatives).
    """

    id: str
    """The unique identifier for the DLC dependency definition.
    """
