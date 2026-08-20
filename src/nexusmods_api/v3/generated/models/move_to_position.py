"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class MoveToPosition(NexusModel):
    """Place the moved versions earlier (`before`) or later (`after`) with..."""

    relative_placement: JsonValue
    """The embedded RelativePlacement data for this MoveToPosition value."""

    target_version_id: str
    """The unique identifier of the version to position relative to."""
