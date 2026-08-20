"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class NewModFileCategory(NexusModel):
    """Models the NewModFileCategory schema from the pinned Nexus Mods REST..."""

    root: JsonValue = None
    """The unstructured value returned for this OpenAPI schema."""
