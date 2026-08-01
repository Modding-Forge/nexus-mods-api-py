"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersionDependencyCandidatesBatchResponse(NexusModel):
    """Provides a generated Pydantic response model."""

    candidates: list[JsonValue]
