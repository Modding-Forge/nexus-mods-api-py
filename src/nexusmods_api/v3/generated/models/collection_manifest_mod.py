"""Copyright (c) Modding Forge."""

from typing import Optional

from ....models.nexus_model import NexusModel
from ....types import JsonValue


class CollectionManifestMod(NexusModel):
    """Provides a generated Pydantic response model."""

    author: Optional[str] = None
    domain_name: str
    name: str
    optional: bool
    source: JsonValue
    version: str
