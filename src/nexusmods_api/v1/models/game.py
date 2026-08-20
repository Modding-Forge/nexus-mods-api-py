"""Copyright (c) Modding Forge."""

from typing import Optional

from ...models.nexus_model import NexusModel
from .game_category import GameCategory


class Game(NexusModel):
    """Describes a game and, when requested, its mod categories."""

    id: int
    """The unique Nexus Mods game identifier."""
    domain_name: str
    """The game domain used in Nexus Mods URLs and API paths."""
    name: str
    """The game's display name."""
    name_lower: Optional[str] = None
    """The normalized lowercase game name, when reported."""
    forum_url: Optional[str] = None
    """The Nexus Mods forum URL for the game, when available."""
    nexusmods_url: Optional[str] = None
    """The Nexus Mods landing-page URL for the game, when available."""
    genre: Optional[str] = None
    """The game's genre, when reported."""
    file_count: Optional[int] = None
    """The number of files hosted for the game, when reported."""
    downloads: Optional[int] = None
    """The total number of downloads for the game, when reported."""
    mods: Optional[int] = None
    """The number of mods hosted for the game, when reported."""
    categories: Optional[list[GameCategory]] = None
    """The game's mod categories, when requested from the API."""
