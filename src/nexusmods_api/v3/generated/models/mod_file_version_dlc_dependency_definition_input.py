"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class ModFileVersionDlcDependencyDefinitionInput(NexusModel):
    """Models the ModFileVersionDlcDependencyDefinitionInput schema from the..."""

    dlc_ids: list[str]
    """The DLC ids that satisfy this definition (OR-alternatives). Must be..."""
