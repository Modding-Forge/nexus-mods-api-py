"""Copyright (c) Modding Forge."""

from typing import Optional

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class MinimalMod(NexusModel):
    """A minimal representation of a mod."""

    adult_content: Optional[bool] = None
    """Whether the mod is marked as adult content.
    """

    game: JsonValue
    """The embedded MinimalGame data for this MinimalMod value.
    """

    game_scoped_id: str
    """The game-scoped identifier for the mod.
    """

    id: str
    """The unique identifier for the mod.
    """

    name: str
    """The name of the mod.
    """

    status: Optional[JsonValue] = None
    """The embedded ModStatus data for this MinimalMod value.
    """

    thumbnail_url: Optional[str] = None
    """The URL of the mod's thumbnail image.
    """
