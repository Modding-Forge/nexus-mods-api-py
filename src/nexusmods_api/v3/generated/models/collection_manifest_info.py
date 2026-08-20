"""Copyright (c) Modding Forge."""

from typing import Optional

from ....models.nexus_model import NexusModel


class CollectionManifestInfo(NexusModel):
    """The info section of the JSON manifest."""

    author: str
    """The collection author's name."""

    author_url: Optional[str] = None
    """The url of the author's profile."""

    description: Optional[str] = None
    """A description of the collection."""

    domain_name: str
    """The domain name of the game."""

    game_versions: Optional[list[str]] = None
    """A list of game versions that this revision has been tested with."""

    name: str
    """The name of the collection."""

    summary: Optional[str] = None
    """A short summary of the collection."""
