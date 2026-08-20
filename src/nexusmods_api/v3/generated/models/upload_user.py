"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class UploadUser(NexusModel):
    """Models the UploadUser schema from the pinned Nexus Mods REST v3..."""

    id: str
    """The unique identifier for the user who owns this upload."""
