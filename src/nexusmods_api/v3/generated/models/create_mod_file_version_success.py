"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class CreateModFileVersionSuccess(NexusModel):
    """Provides a generated Pydantic response model."""

    file: JsonValue
    version: JsonValue
