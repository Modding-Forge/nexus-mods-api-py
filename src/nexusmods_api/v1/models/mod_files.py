"""Copyright (c) Modding Forge."""

from ...models.nexus_model import NexusModel
from .file_update import FileUpdate
from .mod_file import ModFile


class ModFiles(NexusModel):
    """Groups all files and author-declared file replacements for a mod."""

    files: list[ModFile]
    """The files currently exposed for the mod."""
    file_updates: list[FileUpdate]
    """The replacement relationships between old and current files."""
