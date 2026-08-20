"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class RevisionStatus(NexusModel):
    """The status of a collection revision."""

    root: JsonValue = None
    """The unstructured value returned for this OpenAPI schema."""
