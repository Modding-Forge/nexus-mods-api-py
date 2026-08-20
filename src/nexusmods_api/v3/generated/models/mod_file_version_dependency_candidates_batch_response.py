"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersionDependencyCandidatesBatchResponse(NexusModel):
    """Models the ModFileVersionDependencyCandidatesBatchResponse schema..."""

    candidates: list[JsonValue]
    """The embedded ModFileVersionDependencyCandidate data for this..."""
