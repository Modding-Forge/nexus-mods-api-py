"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class CreateCollectionRequest(NexusModel):
    """Models the CreateCollectionRequest schema from the pinned Nexus Mods..."""

    collection_data: JsonValue
    """The embedded CollectionPayload data for this CreateCollectionRequest..."""

    upload_id: str
    """The unique identifier for the upload to claim against this new..."""
