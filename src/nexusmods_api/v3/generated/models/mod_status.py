"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModStatus(NexusModel):
    """The effective visibility status of a mod."""

    root: JsonValue = None
    """The unstructured value returned for this OpenAPI schema."""
