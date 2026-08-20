"""Copyright (c) Modding Forge."""

from typing import Optional

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersion(NexusModel):
    """A single version of a mod file, merging the physical file and its..."""

    category: JsonValue
    """The embedded ModFileCategory data for this ModFileVersion value."""

    file: JsonValue
    """The embedded ModFile data for this ModFileVersion value."""

    game_scoped_id: str
    """The game-scoped identifier for the mod file version."""

    id: str
    """The unique identifier for the mod file version."""

    is_primary: Optional[bool] = None
    """Whether this version is the primary file for the mod. The primary..."""

    name: str
    """The name of the mod file version."""

    position: str
    """Position within the mod file."""

    uploaded_at: str
    """The date and time the version was uploaded."""

    version: str
    """The version string of the mod file version."""
