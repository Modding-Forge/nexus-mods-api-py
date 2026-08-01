"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class CreateUploadSuccess(NexusModel):
    """Provides a generated Pydantic response model."""

    presigned_url: str
