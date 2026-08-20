"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class CreateUploadRequest(NexusModel):
    """Models the CreateUploadRequest schema from the pinned Nexus Mods REST..."""

    filename: str
    """User-defined filename."""

    size_bytes: int
    """Size of file in bytes."""
