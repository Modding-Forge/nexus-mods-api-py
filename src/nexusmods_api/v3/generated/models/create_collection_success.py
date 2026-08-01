"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class CreateCollectionSuccess(NexusModel):
    """Provides a generated Pydantic response model."""

    id: str
    revision_id: str
    revision_number: int
    revision_status: JsonValue
    slug: str
