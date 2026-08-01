"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class Dlc(NexusModel):
    """Provides a generated Pydantic response model."""

    id: str
    name: str
    thumbnail_url: str
