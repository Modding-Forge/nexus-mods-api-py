"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class CollectionPayload(NexusModel):
    """The data payload used to create a collection revision."""

    adult_content: bool
    """Whether the collection includes adult content."""

    collection_manifest: JsonValue
    """The embedded CollectionManifest data for this CollectionPayload value."""

    collection_schema_id: int
    """Collection schema id."""
