"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileCategory(NexusModel):
    """Provides a generated Pydantic response model."""

    root: JsonValue = None
