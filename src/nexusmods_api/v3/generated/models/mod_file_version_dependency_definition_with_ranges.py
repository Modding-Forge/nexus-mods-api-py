"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersionDependencyDefinitionWithRanges(NexusModel):
    """Provides a generated Pydantic response model."""

    id: str
    ranges: list[JsonValue]
