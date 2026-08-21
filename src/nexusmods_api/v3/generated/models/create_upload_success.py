"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class CreateUploadSuccess(NexusModel):
    """Models the CreateUploadSuccess REST v3 schema.

    Models the CreateUploadSuccess schema from the pinned Nexus Mods REST v3 OpenAPI doc\
ument.
    """

    presigned_url: str
    """Presigned URL.
    """
