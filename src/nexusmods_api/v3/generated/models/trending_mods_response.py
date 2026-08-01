"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class TrendingModsResponse(NexusModel):
    """Provides a generated Pydantic response model."""

    mods: list[JsonValue]
