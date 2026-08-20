"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class CreateUpdateGroupVersionSuccess(NexusModel):
    """Models the CreateUpdateGroupVersionSuccess schema from the pinned..."""

    root: JsonValue = None
    """The unstructured value returned for this OpenAPI schema."""
