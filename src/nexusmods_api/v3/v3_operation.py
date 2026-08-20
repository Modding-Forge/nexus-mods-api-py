"""Copyright (c) Modding Forge."""

from pydantic import ConfigDict

from ..models.nexus_model import NexusModel


class V3Operation(NexusModel):
    """Describes one operation generated from the pinned OpenAPI snapshot."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    operation_id: str
    """The stable OpenAPI operation identifier."""
    method: str
    """The uppercase HTTP method used by the operation."""
    path: str
    """The relative REST v3 path template."""
    path_parameters: tuple[str, ...]
    """The ordered path parameter names required by the operation."""
    has_body: bool
    """Whether the operation accepts a JSON request body."""
    experimental: bool
    """Whether the operation is marked experimental by Nexus Mods."""
    deprecated: bool
    """Whether the operation is marked deprecated by Nexus Mods."""
