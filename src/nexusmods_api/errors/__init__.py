"""Copyright (c) Modding Forge."""

from .nexus_api_error import NexusApiError
from .nexus_authentication_error import NexusAuthenticationError
from .nexus_graphql_error import NexusGraphQLError
from .nexus_http_error import NexusHttpError
from .nexus_oauth_error import NexusOAuthError
from .nexus_rate_limit_error import NexusRateLimitError
from .nexus_response_validation_error import NexusResponseValidationError
from .nexus_sso_error import NexusSSOError
from .nexus_transport_error import NexusTransportError

__all__: list[str] = [
    "NexusApiError",
    "NexusAuthenticationError",
    "NexusGraphQLError",
    "NexusHttpError",
    "NexusOAuthError",
    "NexusRateLimitError",
    "NexusResponseValidationError",
    "NexusSSOError",
    "NexusTransportError",
]
