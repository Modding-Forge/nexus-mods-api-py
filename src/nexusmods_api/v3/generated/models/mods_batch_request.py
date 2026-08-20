"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class ModsBatchRequest(NexusModel):
    """Models the ModsBatchRequest schema from the pinned Nexus Mods REST v3..."""

    mod_ids: list[str]
    """Composite mod UIDs (gameId << 32 | modId) to resolve. Same id space..."""
