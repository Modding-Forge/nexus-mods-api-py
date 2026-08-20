"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class CreateCollectionSuccess(NexusModel):
    """Models the CreateCollectionSuccess schema from the pinned Nexus Mods..."""

    id: str
    """The unique identifier for the collection."""

    revision_id: str
    """The unique identifier for the initial collection revision."""

    revision_number: int
    """The revision number."""

    revision_status: JsonValue
    """The embedded RevisionStatus data for this CreateCollectionSuccess value."""

    slug: str
    """The slug for the collection."""
