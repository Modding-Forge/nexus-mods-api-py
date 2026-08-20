"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class UpdatePolicy(NexusModel):
    """Available update policies of a file resource."""

    root: JsonValue = None
    """The unstructured value returned for this OpenAPI schema."""
