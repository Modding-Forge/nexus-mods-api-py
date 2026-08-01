"""Copyright (c) Modding Forge."""

from .nexus_http_error import NexusHttpError


class NexusAuthenticationError(NexusHttpError):
    """Indicates rejected or insufficient Nexus Mods authentication."""
