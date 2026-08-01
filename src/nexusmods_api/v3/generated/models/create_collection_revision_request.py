"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class CreateCollectionRevisionRequest(NexusModel):
    """Provides a generated Pydantic response model."""

    collection_data: JsonValue
    upload_id: str
