"""Copyright (c) Modding Forge."""

from typing import Optional

from ...models.nexus_model import NexusModel


class GameCategory(NexusModel):
    """Describes one Nexus Mods category for a game."""

    category_id: int
    name: str
    parent_category: Optional[int | bool] = None
