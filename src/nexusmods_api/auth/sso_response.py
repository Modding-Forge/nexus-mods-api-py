"""Copyright (c) Modding Forge."""

from typing import Optional

from pydantic import Field

from ..models.nexus_model import NexusModel
from .sso_response_data import SSOResponseData


class SSOResponse(NexusModel):
    """Models one structured Nexus Mods SSO protocol response."""

    success: bool
    """Whether Nexus Mods accepted the protocol operation."""

    data: SSOResponseData = Field(default_factory=SSOResponseData)
    """The successful response values returned by Nexus Mods."""

    error: Optional[object] = None
    """Provider error metadata that is never exposed to callers."""
