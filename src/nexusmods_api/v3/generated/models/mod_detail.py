"""Copyright (c) Modding Forge."""

from typing import Optional

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModDetail(NexusModel):
    """Provides a generated Pydantic response model."""

    adult_content: bool
    game_id: str
    id: str
    name: str
    status: JsonValue
    summary: str
    thumbnail_url: Optional[str] = None
