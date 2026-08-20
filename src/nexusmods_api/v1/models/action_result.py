"""Copyright (c) Modding Forge."""

from typing import Optional

from ...models.nexus_model import NexusModel


class ActionResult(NexusModel):
    """Describes the result of a v1 tracking or endorsement mutation."""

    message: str
    """The human-readable result message returned by Nexus Mods."""
    status: Optional[str] = None
    """The optional machine-readable result status."""
