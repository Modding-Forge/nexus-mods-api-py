"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersionDlcDependencyDefinition(NexusModel):
    """Provides a generated Pydantic response model."""

    dlc_targets: list[JsonValue]
    id: str
