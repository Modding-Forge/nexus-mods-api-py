"""Copyright (c) Modding Forge."""

from typing import Optional

from ....models.nexus_model import NexusModel


class ModFileVersionDependencyRangeInput(NexusModel):
    """Models the ModFileVersionDependencyRangeInput schema from the pinned..."""

    max_version_id: Optional[str] = None
    """The ID of the mod file version representing the upper bound of the..."""

    min_version_id: str
    """The ID of the mod file version representing the lower bound of the..."""
