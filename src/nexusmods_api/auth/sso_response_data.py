"""Copyright (c) Modding Forge."""

from typing import Optional

from pydantic import SecretStr

from ..models.nexus_model import NexusModel


class SSOResponseData(NexusModel):
    """Models the secret-bearing values in an SSO v2 response."""

    connection_token: Optional[SecretStr] = None
    """The masked token that Nexus Mods issues for reconnecting a session."""

    api_key: Optional[SecretStr] = None
    """The masked application-specific API key issued after authorization."""
