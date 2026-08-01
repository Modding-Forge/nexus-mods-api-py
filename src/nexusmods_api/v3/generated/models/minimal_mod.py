"""Copyright (c) Modding Forge."""

from typing import Optional

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class MinimalMod(NexusModel):
    """Provides a generated Pydantic response model."""

    adult_content: Optional[bool] = None
    game: JsonValue
    game_scoped_id: str
    id: str
    name: str
    status: Optional[JsonValue] = None
    thumbnail_url: Optional[str] = None
