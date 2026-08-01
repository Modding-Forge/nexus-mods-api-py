"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class RevisionStatus(NexusModel):
    """Provides a generated Pydantic response model."""

    root: JsonValue = None
