"""Copyright (c) Modding Forge."""

from typing import Optional

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class CollectionManifestModSource(NexusModel):
    """Provides a generated Pydantic response model."""

    adult_content: Optional[bool] = None
    file_expression: Optional[str] = None
    file_id: Optional[str] = None
    file_size: Optional[int] = None
    logical_filename: Optional[str] = None
    md5: Optional[str] = None
    mod_id: Optional[str] = None
    type: JsonValue
    update_policy: Optional[JsonValue] = None
    url: Optional[str] = None
