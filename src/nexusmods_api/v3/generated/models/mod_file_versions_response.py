"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersionsResponse(NexusModel):
    """Provides a generated Pydantic response model."""

    versions: list[JsonValue]
