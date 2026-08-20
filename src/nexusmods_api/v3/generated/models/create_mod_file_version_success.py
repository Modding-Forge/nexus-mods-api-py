"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class CreateModFileVersionSuccess(NexusModel):
    """Models the CreateModFileVersionSuccess schema from the pinned Nexus..."""

    file: JsonValue
    """The embedded UploadModFile data for this CreateModFileVersionSuccess..."""

    version: JsonValue
    """The embedded CreatedModFileVersion data for this..."""
