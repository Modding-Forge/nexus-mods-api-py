"""Copyright (c) Modding Forge."""

from typing import Optional

from ....models.nexus_model import NexusModel


class Mod(NexusModel):
    """Models the Mod schema from the pinned Nexus Mods REST v3 OpenAPI document."""

    game_id: str
    """The unique identifier for game this mod belongs to.
    """

    game_scoped_id: str
    """The game-scoped identifier for the mod.
    """

    id: str
    """The unique identifier for the mod.
    """

    name: Optional[str] = None
    """Mod name (only shown if mod is available).
    """
