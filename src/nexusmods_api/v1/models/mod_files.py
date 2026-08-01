"""Copyright (c) Modding Forge."""

from ...models.nexus_model import NexusModel
from .file_update import FileUpdate
from .mod_file import ModFile


class ModFiles(NexusModel):
    """Groups all files and author-declared file replacements for a mod."""

    files: list[ModFile]
    file_updates: list[FileUpdate]
