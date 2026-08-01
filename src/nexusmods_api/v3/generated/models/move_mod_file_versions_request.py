"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class MoveModFileVersionsRequest(NexusModel):
    """Provides a generated Pydantic response model."""

    target: JsonValue
    version_ids: list[str]
