"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class GameDlcsResponse(NexusModel):
    """Provides a generated Pydantic response model."""

    dlcs: list[JsonValue]
