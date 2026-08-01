"""Copyright (c) Modding Forge."""

from ...models.nexus_model import NexusModel


class ColourScheme(NexusModel):
    """Describes one legacy Nexus Mods site colour scheme."""

    id: int
    name: str
    primary_colour: str
    secondary_colour: str
    darker_colour: str
