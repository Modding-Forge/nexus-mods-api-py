"""Copyright (c) Modding Forge."""

from typing import Optional

from ....models.nexus_model import NexusModel


class ModFileVersionDependencyRangeInput(NexusModel):
    """Models the ModFileVersionDependencyRangeInput REST v3 schema.

    Models the ModFileVersionDependencyRangeInput schema from the pinned Nexus Mods REST\
 v3 OpenAPI document.
    """

    max_version_id: Optional[str] = None
    """The ID of the mod file version representing the upper bound of the range. Null me\
ans open-ended (no upper bound).
    """

    min_version_id: str
    """The ID of the mod file version representing the lower bound of the range.
    """
