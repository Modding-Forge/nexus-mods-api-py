"""Copyright (c) Modding Forge."""

from typing import Optional

from ...models.nexus_model import NexusModel


class GameCategory(NexusModel):
    """Describes one Nexus Mods category for a game."""

    category_id: int
    """The unique game-category identifier."""
    name: str
    """The display name of the game category."""
    parent_category: Optional[int | bool] = None
    """The parent category identifier, or a false value for a root category."""
