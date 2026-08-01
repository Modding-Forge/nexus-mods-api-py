"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class DependencyCandidateModFile(NexusModel):
    """Provides a generated Pydantic response model."""

    candidate_versions: list[JsonValue]
    id: str
    mod: JsonValue
    name: str
