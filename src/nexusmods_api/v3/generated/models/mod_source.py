"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModSource(NexusModel):
    """Used to define the source of a mod. Useful for informing Collections..."""

    root: JsonValue = None
    """The unstructured value returned for this OpenAPI schema."""
