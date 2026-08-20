"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class MoveModFileVersionsToNewModFileRequest(NexusModel):
    """Models the MoveModFileVersionsToNewModFileRequest schema from the..."""

    mod_file_name: str
    """The name of the new mod file."""

    version_ids: list[str]
    """The unique identifiers for the mod file versions to move. Versions..."""
