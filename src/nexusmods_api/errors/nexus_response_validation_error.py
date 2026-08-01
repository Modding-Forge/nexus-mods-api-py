"""Copyright (c) Modding Forge."""

from .nexus_api_error import NexusApiError


class NexusResponseValidationError(NexusApiError):
    """Indicates that an upstream payload violated its response model."""
