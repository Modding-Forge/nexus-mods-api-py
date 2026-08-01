"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class ModFileVersionDependencyCandidate(NexusModel):
    """Provides a generated Pydantic response model."""

    category: JsonValue
    definition_id: str
    mod_file_id: str
    mod_id: str
    mod_status: JsonValue
    position: str
    source_version_id: str
    version_id: str
