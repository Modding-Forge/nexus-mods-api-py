"""Copyright (c) Modding Forge."""

from .nexus_api_error import NexusApiError


class NexusTransportError(NexusApiError):
    """Indicates that an HTTP exchange could not be completed."""
