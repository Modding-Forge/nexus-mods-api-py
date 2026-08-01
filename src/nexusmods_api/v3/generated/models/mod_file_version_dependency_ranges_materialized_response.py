"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersionDependencyRangesMaterializedResponse(NexusModel):
    """Provides a generated Pydantic response model."""

    dependencies: list[JsonValue]
