"""Copyright (c) Modding Forge."""

from typing import Optional

from ....models.nexus_model import NexusModel


class CollectionManifestInfo(NexusModel):
    """Provides a generated Pydantic response model."""

    author: str
    author_url: Optional[str] = None
    description: Optional[str] = None
    domain_name: str
    game_versions: Optional[list[str]] = None
    name: str
    summary: Optional[str] = None
