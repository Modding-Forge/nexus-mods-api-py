"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class GetModDetails(NexusModel):
    """Models the GetModDetails REST v3 schema.

    Models the GetModDetails schema from the pinned Nexus Mods REST v3 OpenAPI document.
    """

    root: JsonValue = None
    """The unstructured value returned for this OpenAPI schema."""
