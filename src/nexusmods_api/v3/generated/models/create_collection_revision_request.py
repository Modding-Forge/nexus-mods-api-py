"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class CreateCollectionRevisionRequest(NexusModel):
    """Models the CreateCollectionRevisionRequest schema from the pinned..."""

    collection_data: JsonValue
    """The embedded CollectionPayload data for this..."""

    upload_id: str
    """The unique identifier for the upload to claim against this new..."""
