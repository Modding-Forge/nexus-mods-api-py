"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class MoveToPosition(NexusModel):
    """Models the MoveToPosition REST v3 schema.

    Place the moved versions earlier (`before`) or later (`after`) with respect to the t\
arget version.
    """

    relative_placement: JsonValue
    """The embedded RelativePlacement data for this MoveToPosition value.
    """

    target_version_id: str
    """The unique identifier of the version to position relative to.
    """
