"""Copyright (c) Modding Forge."""

from typing import Optional

from ...models.nexus_model import NexusModel
from .game_category import GameCategory


class Game(NexusModel):
    """Describes a game and, when requested, its mod categories."""

    id: int
    domain_name: str
    name: str
    name_lower: Optional[str] = None
    forum_url: Optional[str] = None
    nexusmods_url: Optional[str] = None
    genre: Optional[str] = None
    file_count: Optional[int] = None
    downloads: Optional[int] = None
    mods: Optional[int] = None
    categories: Optional[list[GameCategory]] = None
