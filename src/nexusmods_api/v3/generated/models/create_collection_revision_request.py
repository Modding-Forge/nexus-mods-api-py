"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class CreateCollectionRevisionRequest(NexusModel):
    """Models the CreateCollectionRevisionRequest REST v3 schema.

    Models the CreateCollectionRevisionRequest schema from the pinned Nexus Mods REST v3\
 OpenAPI document.
    """

    collection_data: JsonValue
    """The embedded CollectionPayload data for this CreateCollectionRevisionRequest valu\
e.
    """

    upload_id: str
    """The unique identifier for the upload to claim against this new collection.
    """
