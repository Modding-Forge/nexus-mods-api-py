"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class MoveModFileVersionsToNewModFileRequest(NexusModel):
    """Provides a generated Pydantic response model."""

    mod_file_name: str
    version_ids: list[str]
