"""Copyright (c) Modding Forge."""

from typing import Optional

from ....models.nexus_model import NexusModel


class Mod(NexusModel):
    """Provides a generated Pydantic response model."""

    game_id: str
    game_scoped_id: str
    id: str
    name: Optional[str] = None
