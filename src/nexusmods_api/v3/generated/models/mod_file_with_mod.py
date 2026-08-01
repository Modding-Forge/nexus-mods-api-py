"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileWithMod(NexusModel):
    """Provides a generated Pydantic response model."""

    root: JsonValue = None
