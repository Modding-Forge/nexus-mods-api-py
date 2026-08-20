"""Copyright (c) Modding Forge."""

from ...models.nexus_model import NexusModel


class ColourScheme(NexusModel):
    """Describes one legacy Nexus Mods site colour scheme."""

    id: int
    """The unique colour-scheme identifier."""
    name: str
    """The display name of the colour scheme."""
    primary_colour: str
    """The primary colour value supplied by Nexus Mods."""
    secondary_colour: str
    """The secondary colour value supplied by Nexus Mods."""
    darker_colour: str
    """The darker accent colour value supplied by Nexus Mods."""
