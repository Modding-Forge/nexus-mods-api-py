"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class CreateCollectionRevisionSuccess(NexusModel):
    """Provides a generated Pydantic response model."""

    collection_id: str
    id: str
    revision_number: int
    revision_status: JsonValue
