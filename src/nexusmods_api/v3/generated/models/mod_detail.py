"""Copyright (c) Modding Forge."""

from typing import Optional

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModDetail(NexusModel):
    """Mod-level display details. The game-scoped mod id and game id can be..."""

    adult_content: bool
    """Whether the mod is flagged as adult content."""

    game_id: str
    """The id of the game this mod belongs to."""

    id: str
    """Composite mod UID. Echoes the request value so the caller can key..."""

    name: str
    """Mod display name."""

    status: JsonValue
    """The embedded ModStatus data for this ModDetail value."""

    summary: str
    """Sanitised short summary (plain text, as shown on mod cards). Empty..."""

    thumbnail_url: Optional[str] = None
    """Mod thumbnail image URL. Null when the mod has no image, or when..."""
