"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class MinimalGame(NexusModel):
    """Provides a generated Pydantic response model."""

    domain_name: str
    id: str
    name: str
