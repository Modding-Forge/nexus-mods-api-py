"""Copyright (c) Modding Forge."""

from typing import Optional

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class MoveModFileVersionsToNewModFileResponse(NexusModel):
    """The result of a bulk move operation."""

    deleted_source_mod_file_ids: Optional[list[str]] = None
    """A list of IDs for any source mod files that were automatically deleted because th\
ey became
    empty as a result of this move.
    """

    modified_source_mod_files: Optional[list[JsonValue]] = None
    """A list of source mod files that had versions removed but still contain other vers\
ions.
    """

    new_mod_file: JsonValue
    """The embedded ModFileWithAggregates data for this MoveModFileVersionsToNewModFileR\
esponse value.
    """

    versions: list[JsonValue]
    """The updated versions reflecting their new mod file and order.
    """
