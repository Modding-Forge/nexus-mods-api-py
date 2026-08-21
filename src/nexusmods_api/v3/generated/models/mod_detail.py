"""Copyright (c) Modding Forge."""

from typing import Optional

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModDetail(NexusModel):
    """Models the ModDetail REST v3 schema.

    Mod-level display details. The game-scoped mod id and game id can be derived from `i\
d` by
    bit-decomposition (modId = id & 0xFFFFFFFF, gameId = id >> 32); `game_id` is also re\
turned
    directly for convenience.
    """

    adult_content: bool
    """Whether the mod is flagged as adult content.
    """

    game_id: str
    """The id of the game this mod belongs to.
    """

    id: str
    """Composite mod UID. Echoes the request value so the caller can key results back.
    """

    name: str
    """Mod display name.
    """

    status: JsonValue
    """The embedded ModStatus data for this ModDetail value.
    """

    summary: str
    """Sanitised short summary (plain text, as shown on mod cards). Empty string when th\
e mod
    has none.
    """

    thumbnail_url: Optional[str] = None
    """Mod thumbnail image URL. Null when the mod has no image, or when suppressed becau\
se the
    mod is under moderation or removed by staff.
    """
