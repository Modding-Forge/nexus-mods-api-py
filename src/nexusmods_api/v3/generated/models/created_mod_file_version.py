"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class CreatedModFileVersion(NexusModel):
    """Provides a generated Pydantic response model."""

    id: str
    position: str
