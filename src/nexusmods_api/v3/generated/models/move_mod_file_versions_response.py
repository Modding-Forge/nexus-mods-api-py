"""Copyright (c) Modding Forge."""

from typing import Optional

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class MoveModFileVersionsResponse(NexusModel):
    """The result of a bulk move operation."""

    deleted_source_mod_file_ids: Optional[list[str]] = None
    """A list of IDs for any source mod files that were automatically..."""

    modified_source_mod_files: Optional[list[JsonValue]] = None
    """A list of source mod files that had versions removed but still..."""

    target_mod_file: JsonValue
    """The embedded ModFileWithAggregates data for this..."""

    versions: list[JsonValue]
    """The updated versions reflecting their new mod file and order."""
