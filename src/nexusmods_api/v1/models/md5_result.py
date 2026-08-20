"""Copyright (c) Modding Forge."""

from ...models.nexus_model import NexusModel
from .mod import Mod
from .mod_file import ModFile


class MD5Result(NexusModel):
    """Links an MD5 match to its mod and file metadata."""

    mod: Mod
    """The mod associated with the matching file hash."""
    file_details: ModFile
    """The matching file metadata."""
