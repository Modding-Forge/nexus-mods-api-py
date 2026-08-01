"""Copyright (c) Modding Forge."""

from .nexus_api_error import NexusApiError


class NexusSSOError(NexusApiError):
    """Indicates a failed Nexus Mods WebSocket SSO authorization."""
