"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class ModFile(NexusModel):
    """Provides a generated Pydantic response model."""

    id: str
    name: str
