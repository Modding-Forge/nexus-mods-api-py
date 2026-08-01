"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class MoveToPosition(NexusModel):
    """Provides a generated Pydantic response model."""

    relative_placement: JsonValue
    target_version_id: str
