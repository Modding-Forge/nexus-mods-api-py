"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class Dlc(NexusModel):
    """A DLC available for a game."""

    id: str
    """The DLC identifier, scoped to the game."""

    name: str
    """The DLC display name."""

    thumbnail_url: str
    """Thumbnail image URL."""
