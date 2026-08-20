"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersionDependencyRange(NexusModel):
    """Models the ModFileVersionDependencyRange schema from the pinned Nexus..."""

    id: str
    """The unique identifier for the dependency range."""

    max_version: JsonValue
    """The embedded ModFileVersion data for this..."""

    min_version: JsonValue
    """The embedded ModFileVersion data for this..."""

    target_mod_file: JsonValue
    """The embedded ModFileWithMod data for this..."""
