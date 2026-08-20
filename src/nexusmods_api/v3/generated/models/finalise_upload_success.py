"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class FinaliseUploadSuccess(NexusModel):
    """Models the FinaliseUploadSuccess schema from the pinned Nexus Mods..."""

    root: JsonValue = None
    """The unstructured value returned for this OpenAPI schema."""
