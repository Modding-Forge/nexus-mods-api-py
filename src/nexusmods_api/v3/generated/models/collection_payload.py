"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class CollectionPayload(NexusModel):
    """Provides a generated Pydantic response model."""

    adult_content: bool
    collection_manifest: JsonValue
    collection_schema_id: int
