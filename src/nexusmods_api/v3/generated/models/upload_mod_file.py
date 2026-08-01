"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class UploadModFile(NexusModel):
    """Provides a generated Pydantic response model."""

    file_category: JsonValue
    game_scoped_id: str
    id: str
    name: str
