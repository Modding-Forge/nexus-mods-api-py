"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class CreateMultipartUploadSuccess(NexusModel):
    """Provides a generated Pydantic response model."""

    complete_presigned_url: str
    part_presigned_urls: list[str]
    part_size_bytes: int
