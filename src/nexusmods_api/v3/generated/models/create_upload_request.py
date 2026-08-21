"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class CreateUploadRequest(NexusModel):
    """Models the CreateUploadRequest REST v3 schema.

    Models the CreateUploadRequest schema from the pinned Nexus Mods REST v3 OpenAPI doc\
ument.
    """

    filename: str
    """User-defined filename.
    """

    size_bytes: int
    """Size of file in bytes.
    """
