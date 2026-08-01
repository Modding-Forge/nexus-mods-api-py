"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class CollectionManifest(NexusModel):
    """Provides a generated Pydantic response model."""

    info: JsonValue
    mods: list[JsonValue]
