"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class MoveModFileVersionsToNewModFileRequest(NexusModel):
    """Models the MoveModFileVersionsToNewModFileRequest REST v3 schema.

    Models the MoveModFileVersionsToNewModFileRequest schema from the pinned Nexus Mods \
REST v3 OpenAPI document.
    """

    mod_file_name: str
    """The name of the new mod file.
    """

    version_ids: list[str]
    """The unique identifiers for the mod file versions to move.
    Versions are inserted in this order, and `version_ids` is expected to be ordered fro\
m earliest to latest version.
    """
