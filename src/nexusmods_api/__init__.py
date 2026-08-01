"""Copyright (c) Modding Forge."""

from ._version import __version__
from .async_nexus_client import AsyncNexusClient
from .auth.api_key_auth import ApiKeyAuth
from .auth.async_oauth_auth import AsyncOAuthAuth
from .auth.async_oauth_flow import AsyncOAuthFlow
from .auth.async_oauth_loopback import AsyncOAuthLoopbackFlow
from .auth.oauth_auth import OAuthAuth
from .auth.oauth_authorization import OAuthAuthorization
from .auth.oauth_client_config import OAuthClientConfig
from .auth.oauth_credentials import OAuthCredentials
from .auth.oauth_flow import OAuthFlow
from .auth.oauth_loopback import OAuthLoopbackFlow
from .nexus_client import NexusClient
from .nexus_config import NexusConfig
from .v1.async_nexus_v1_client import AsyncNexusV1Client
from .v1.nexus_v1_client import NexusV1Client
from .v2.async_nexus_graphql_client import AsyncNexusGraphQLClient
from .v2.nexus_graphql_client import NexusGraphQLClient
from .v3.async_nexus_v3_client import AsyncNexusV3Client
from .v3.nexus_stability_warning import NexusStabilityWarning
from .v3.nexus_v3_client import NexusV3Client

__all__: list[str] = [
    "ApiKeyAuth",
    "AsyncNexusClient",
    "AsyncNexusGraphQLClient",
    "AsyncNexusV1Client",
    "AsyncNexusV3Client",
    "AsyncOAuthAuth",
    "AsyncOAuthFlow",
    "AsyncOAuthLoopbackFlow",
    "NexusClient",
    "NexusConfig",
    "NexusGraphQLClient",
    "NexusStabilityWarning",
    "NexusV1Client",
    "NexusV3Client",
    "OAuthAuth",
    "OAuthAuthorization",
    "OAuthClientConfig",
    "OAuthCredentials",
    "OAuthFlow",
    "OAuthLoopbackFlow",
    "__version__",
]
