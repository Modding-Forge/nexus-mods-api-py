"""Copyright (c) Modding Forge."""

from .nexus_api_error import NexusApiError


class NexusGraphQLError(NexusApiError):
    """Reports one or more errors returned by the GraphQL endpoint."""
