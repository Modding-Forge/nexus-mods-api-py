"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class CreateUploadSuccess(NexusModel):
    """Models the CreateUploadSuccess schema from the pinned Nexus Mods REST..."""

    presigned_url: str
    """Presigned URL."""
