"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class UpdateModFileVersionDependencyRangesRequest(NexusModel):
    """Provides a generated Pydantic response model."""

    dependency_definitions: list[JsonValue]
