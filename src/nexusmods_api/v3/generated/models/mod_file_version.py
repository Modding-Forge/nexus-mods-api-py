"""Copyright (c) Modding Forge."""

from typing import Optional

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersion(NexusModel):
    """Provides a generated Pydantic response model."""

    category: JsonValue
    file: JsonValue
    game_scoped_id: str
    id: str
    is_primary: Optional[bool] = None
    name: str
    position: str
    uploaded_at: str
    version: str
