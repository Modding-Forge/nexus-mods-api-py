"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class GetModDetails(NexusModel):
    """Models the GetModDetails schema from the pinned Nexus Mods REST v3..."""

    root: JsonValue = None
    """The unstructured value returned for this OpenAPI schema."""
