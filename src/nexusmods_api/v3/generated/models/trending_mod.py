"""Copyright (c) Modding Forge."""

from typing import Optional

from ....models.nexus_model import NexusModel


class TrendingMod(NexusModel):
    """A trending mod entry in the public marketing feed."""

    author: Optional[str] = None
    """The display name of the user who uploaded the mod."""

    mod_page_url: str
    """Canonical URL of the mod page on nexusmods.com."""

    name: str
    """The mod name."""

    picture_url: Optional[str] = None
    """URL of the mod's main image."""

    summary: Optional[str] = None
    """Short summary shown on the mod listing."""
