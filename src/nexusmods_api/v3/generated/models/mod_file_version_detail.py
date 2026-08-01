"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class ModFileVersionDetail(NexusModel):
    """Provides a generated Pydantic response model."""

    id: str
    mod_file_id: str
    mod_id: str
    name: str
    position: str
    version: str
