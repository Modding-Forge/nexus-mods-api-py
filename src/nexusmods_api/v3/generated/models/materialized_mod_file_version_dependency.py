"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class MaterializedModFileVersionDependency(NexusModel):
    """Provides a generated Pydantic response model."""

    candidate_mod_files: list[JsonValue]
    id: str
