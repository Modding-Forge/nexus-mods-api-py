"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class RelativePlacement(NexusModel):
    """`before`: earlier than the target. `after`: later than the target."""

    root: JsonValue = None
    """The unstructured value returned for this OpenAPI schema."""
