"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class Upload(NexusModel):
    """Models the Upload schema from the pinned Nexus Mods REST v3 OpenAPI document."""

    id: str
    """The unique identifier for the upload.
    """

    state: JsonValue
    """The embedded UploadState data for this Upload value.
    """

    user: JsonValue
    """The embedded UploadUser data for this Upload value.
    """
