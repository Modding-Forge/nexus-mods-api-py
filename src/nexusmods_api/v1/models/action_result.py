"""Copyright (c) Modding Forge."""

from typing import Optional

from ...models.nexus_model import NexusModel


class ActionResult(NexusModel):
    """Describes the result of a v1 tracking or endorsement mutation."""

    message: str
    status: Optional[str] = None
