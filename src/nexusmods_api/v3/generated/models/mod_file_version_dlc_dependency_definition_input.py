"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class ModFileVersionDlcDependencyDefinitionInput(NexusModel):
    """Models the ModFileVersionDlcDependencyDefinitionInput REST v3 schema.

    Models the ModFileVersionDlcDependencyDefinitionInput schema from the pinned Nexus M\
ods REST v3 OpenAPI document.
    """

    dlc_ids: list[str]
    """The DLC ids that satisfy this definition (OR-alternatives). Must be non-empty
    and contain no duplicates. Each id must reference a DLC available for the
    version's game.
    """
