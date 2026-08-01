"""Copyright (c) Modding Forge."""

from typing import Optional

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class MoveModFileVersionsToNewModFileResponse(NexusModel):
    """Provides a generated Pydantic response model."""

    deleted_source_mod_file_ids: Optional[list[str]] = None
    modified_source_mod_files: Optional[list[JsonValue]] = None
    new_mod_file: JsonValue
    versions: list[JsonValue]
