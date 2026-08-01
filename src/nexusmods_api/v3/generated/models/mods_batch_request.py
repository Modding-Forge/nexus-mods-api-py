"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class ModsBatchRequest(NexusModel):
    """Provides a generated Pydantic response model."""

    mod_ids: list[str]
