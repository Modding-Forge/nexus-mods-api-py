"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersionDependenciesResponse(NexusModel):
    """Provides a generated Pydantic response model."""

    dependency_definitions: list[JsonValue]
    dlc_dependency_definitions: list[JsonValue]
