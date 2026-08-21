"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersionDependencyCandidatesBatchResponse(NexusModel):
    """Models the ModFileVersionDependencyCandidatesBatchResponse REST v3 schema.

    Models the ModFileVersionDependencyCandidatesBatchResponse schema from the pinned Ne\
xus Mods REST v3 OpenAPI document.
    """

    candidates: list[JsonValue]
    """The embedded ModFileVersionDependencyCandidate data for this ModFileVersionDepend\
encyCandidatesBatchResponse value.
    """
