"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class CreateCollectionRequest(NexusModel):
    """Provides a generated Pydantic response model."""

    collection_data: JsonValue
    upload_id: str
