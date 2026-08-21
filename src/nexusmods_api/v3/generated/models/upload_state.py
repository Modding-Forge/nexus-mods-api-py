"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class UploadState(NexusModel):
    """Models the UploadState REST v3 schema.

    Models the UploadState schema from the pinned Nexus Mods REST v3 OpenAPI document.
    """

    root: JsonValue = None
    """The unstructured value returned for this OpenAPI schema."""
