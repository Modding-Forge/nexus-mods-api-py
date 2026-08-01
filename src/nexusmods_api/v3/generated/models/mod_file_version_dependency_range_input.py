"""Copyright (c) Modding Forge."""

from typing import Optional

from ....models.nexus_model import NexusModel


class ModFileVersionDependencyRangeInput(NexusModel):
    """Provides a generated Pydantic response model."""

    max_version_id: Optional[str] = None
    min_version_id: str
