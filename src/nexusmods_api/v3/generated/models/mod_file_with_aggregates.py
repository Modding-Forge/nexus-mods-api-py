"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileWithAggregates(NexusModel):
    """A mod file enriched with aggregate stats across its versions."""

    root: JsonValue = None
    """The unstructured value returned for this OpenAPI schema."""
