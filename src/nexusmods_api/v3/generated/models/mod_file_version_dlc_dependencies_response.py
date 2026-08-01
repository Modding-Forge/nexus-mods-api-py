"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersionDlcDependenciesResponse(NexusModel):
    """Provides a generated Pydantic response model."""

    dlc_dependency_definitions: list[JsonValue]
