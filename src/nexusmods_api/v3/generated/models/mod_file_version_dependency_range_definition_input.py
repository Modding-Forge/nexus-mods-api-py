"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersionDependencyRangeDefinitionInput(NexusModel):
    """Provides a generated Pydantic response model."""

    ranges: list[JsonValue]
