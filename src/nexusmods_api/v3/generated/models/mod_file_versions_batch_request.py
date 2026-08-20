"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class ModFileVersionsBatchRequest(NexusModel):
    """Models the ModFileVersionsBatchRequest schema from the pinned Nexus..."""

    version_ids: list[str]
    """The mod file version ids to resolve details for."""
