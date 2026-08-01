"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class ModFileVersionsBatchRequest(NexusModel):
    """Provides a generated Pydantic response model."""

    version_ids: list[str]
