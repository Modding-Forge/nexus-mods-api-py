"""Copyright (c) Modding Forge."""

from .nexus_http_error import NexusHttpError


class NexusRateLimitError(NexusHttpError):
    """Indicates that the Nexus Mods request limit was exhausted."""
