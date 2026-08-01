"""Copyright (c) Modding Forge."""

from typing import Optional

from ....models.nexus_model import NexusModel


class TrendingMod(NexusModel):
    """Provides a generated Pydantic response model."""

    author: Optional[str] = None
    mod_page_url: str
    name: str
    picture_url: Optional[str] = None
    summary: Optional[str] = None
