"""Copyright (c) Modding Forge."""

from typing import Optional

from ....models.nexus_model import NexusModel


class ModFileVersionDependencyCandidatesBatchRequest(NexusModel):
    """Models the ModFileVersionDependencyCandidatesBatchRequest schema from..."""

    page: Optional[int] = None
    """Page number (1-indexed)."""

    page_size: Optional[int] = None
    """Number of candidate rows per page."""

    version_ids: list[str]
    """The source mod file version ids to resolve dependency candidates for...."""
