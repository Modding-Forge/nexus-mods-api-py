"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileCategory(NexusModel):
    """Models the ModFileCategory REST v3 schema.

    Models the ModFileCategory schema from the pinned Nexus Mods REST v3 OpenAPI documen\
t.
    """

    root: JsonValue = None
    """The unstructured value returned for this OpenAPI schema."""
