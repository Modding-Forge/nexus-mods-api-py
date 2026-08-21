"""Copyright (c) Modding Forge."""

from ....models.nexus_model import NexusModel


class MinimalGame(NexusModel):
    """A minimal representation of a game."""

    domain_name: str
    """The URL-friendly slug for the game.
    """

    id: str
    """The unique identifier for the game.
    """

    name: str
    """The name of the game.
    """
