"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersionDependencyRangesResponse(NexusModel):
    """Provides a generated Pydantic response model."""

    dependency_definitions: list[JsonValue]
