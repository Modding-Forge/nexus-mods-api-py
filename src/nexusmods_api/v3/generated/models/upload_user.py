"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class UploadUser(NexusModel):
    """Models the UploadUser REST v3 schema.

    Models the UploadUser schema from the pinned Nexus Mods REST v3 OpenAPI document.
    """

    id: str
    """The unique identifier for the user who owns this upload.
    """
