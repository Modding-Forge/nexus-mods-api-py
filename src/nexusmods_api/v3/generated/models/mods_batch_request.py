"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class ModsBatchRequest(NexusModel):
    """Models the ModsBatchRequest REST v3 schema.

    Models the ModsBatchRequest schema from the pinned Nexus Mods REST v3 OpenAPI docume\
nt.
    """

    mod_ids: list[str]
    """Composite mod UIDs (gameId << 32 | modId) to resolve. Same id space as the `mod_i\
d`
    returned by the dependency candidates and mod file version batch endpoints.
    """
