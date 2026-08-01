"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFilesResponse(NexusModel):
    """Provides a generated Pydantic response model."""

    mod_files: list[JsonValue]
