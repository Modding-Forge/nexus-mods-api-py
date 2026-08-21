"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class CreateModFileVersionSuccess(NexusModel):
    """Models the CreateModFileVersionSuccess REST v3 schema.

    Models the CreateModFileVersionSuccess schema from the pinned Nexus Mods REST v3 Ope\
nAPI document.
    """

    file: JsonValue
    """The embedded UploadModFile data for this CreateModFileVersionSuccess value.
    """

    version: JsonValue
    """The embedded CreatedModFileVersion data for this CreateModFileVersionSuccess valu\
e.
    """
