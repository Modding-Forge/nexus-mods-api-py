"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersionDependencyRange(NexusModel):
    """Provides a generated Pydantic response model."""

    id: str
    max_version: JsonValue
    min_version: JsonValue
    target_mod_file: JsonValue
