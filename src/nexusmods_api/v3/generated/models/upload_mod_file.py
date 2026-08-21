"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class UploadModFile(NexusModel):
    """Models the UploadModFile REST v3 schema.

    Models the UploadModFile schema from the pinned Nexus Mods REST v3 OpenAPI document.
    """

    file_category: JsonValue
    """The embedded NewModFileCategory data for this UploadModFile value.
    """

    game_scoped_id: str
    """The game-scoped identifier for the mod file.
    """

    id: str
    """The unique identifier for the mod file.
    """

    name: str
    """Mod file name.
    """
