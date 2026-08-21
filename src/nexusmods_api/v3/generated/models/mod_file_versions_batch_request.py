"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class ModFileVersionsBatchRequest(NexusModel):
    """Models the ModFileVersionsBatchRequest REST v3 schema.

    Models the ModFileVersionsBatchRequest schema from the pinned Nexus Mods REST v3 Ope\
nAPI document.
    """

    version_ids: list[str]
    """The mod file version ids to resolve details for.
    """
