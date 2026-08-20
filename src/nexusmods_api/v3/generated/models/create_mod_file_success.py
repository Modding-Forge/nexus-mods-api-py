"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class CreateModFileSuccess(NexusModel):
    """Models the CreateModFileSuccess schema from the pinned Nexus Mods..."""

    root: JsonValue = None
    """The unstructured value returned for this OpenAPI schema."""
