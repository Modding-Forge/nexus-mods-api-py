"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileCategory(NexusModel):
    """Models the ModFileCategory schema from the pinned Nexus Mods REST v3..."""

    root: JsonValue = None
    """The unstructured value returned for this OpenAPI schema."""
