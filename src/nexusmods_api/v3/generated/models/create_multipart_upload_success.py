"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class CreateMultipartUploadSuccess(NexusModel):
    """Models the CreateMultipartUploadSuccess schema from the pinned Nexus..."""

    complete_presigned_url: str
    """Presigned URL to complete upload."""

    part_presigned_urls: list[str]
    """Presigned URLs for each upload part."""

    part_size_bytes: int
    """Size of each part in bytes."""
