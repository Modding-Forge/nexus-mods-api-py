"""Copyright (c) Modding Forge."""

from typing import Optional

from ....models.nexus_model import NexusModel


class ModFileVersionDependencyCandidatesBatchRequest(NexusModel):
    """Provides a generated Pydantic response model."""

    page: Optional[int] = None
    page_size: Optional[int] = None
    version_ids: list[str]
