"""Copyright (c) Modding Forge."""

from .nexus_api_error import NexusApiError


class NexusHttpError(NexusApiError):
    """Indicates a final unsuccessful Nexus Mods HTTP response."""
