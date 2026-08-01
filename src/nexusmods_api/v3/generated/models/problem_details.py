"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class ProblemDetails(NexusModel):
    """Provides a generated Pydantic response model."""

    detail: str
    instance: str
    status: int
    title: str
    type: str
