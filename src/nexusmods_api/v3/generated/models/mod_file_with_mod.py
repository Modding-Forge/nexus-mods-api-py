"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileWithMod(NexusModel):
    """A mod file with its associated mod."""

    root: JsonValue = None
    """The unstructured value returned for this OpenAPI schema."""
