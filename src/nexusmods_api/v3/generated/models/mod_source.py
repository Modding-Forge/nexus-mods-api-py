"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModSource(NexusModel):
    """Models the ModSource REST v3 schema.

    Used to define the source of a mod. Useful for informing Collections how to retrieve\
 mods.
    """

    root: JsonValue = None
    """The unstructured value returned for this OpenAPI schema."""
