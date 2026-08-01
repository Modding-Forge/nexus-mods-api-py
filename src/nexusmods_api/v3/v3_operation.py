"""Copyright (c) Modding Forge."""

from pydantic import ConfigDict

from ..models.nexus_model import NexusModel


class V3Operation(NexusModel):
    """Describes one operation generated from the pinned OpenAPI snapshot."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    operation_id: str
    method: str
    path: str
    path_parameters: tuple[str, ...]
    has_body: bool
    experimental: bool
    deprecated: bool
