"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class CreateUploadRequest(NexusModel):
    """Provides a generated Pydantic response model."""

    filename: str
    size_bytes: int
