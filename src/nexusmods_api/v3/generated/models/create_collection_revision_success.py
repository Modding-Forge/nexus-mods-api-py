"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class CreateCollectionRevisionSuccess(NexusModel):
    """Models the CreateCollectionRevisionSuccess REST v3 schema.

    Models the CreateCollectionRevisionSuccess schema from the pinned Nexus Mods REST v3\
 OpenAPI document.
    """

    collection_id: str
    """The unique identifier for the collection this revision belongs to.
    """

    id: str
    """The unique identifier for the revision.
    """

    revision_number: int
    """The revision number.
    """

    revision_status: JsonValue
    """The embedded RevisionStatus data for this CreateCollectionRevisionSuccess value.
    """
