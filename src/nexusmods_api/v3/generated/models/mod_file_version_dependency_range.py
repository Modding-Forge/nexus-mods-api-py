"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersionDependencyRange(NexusModel):
    """Models the ModFileVersionDependencyRange REST v3 schema.

    Models the ModFileVersionDependencyRange schema from the pinned Nexus Mods REST v3 O\
penAPI document.
    """

    id: str
    """The unique identifier for the dependency range.
    """

    max_version: JsonValue
    """The embedded ModFileVersion data for this ModFileVersionDependencyRange value.
    """

    min_version: JsonValue
    """The embedded ModFileVersion data for this ModFileVersionDependencyRange value.
    """

    target_mod_file: JsonValue
    """The embedded ModFileWithMod data for this ModFileVersionDependencyRange value.
    """
