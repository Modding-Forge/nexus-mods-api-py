"""Copyright (c) Modding Forge."""

from typing import Optional

import httpx

from .auth.api_key_auth import ApiKeyAuth
from .auth.oauth_auth import OAuthAuth
from .nexus_config import NexusConfig
from .v1.nexus_v1_client import NexusV1Client
from .v2.nexus_graphql_client import NexusGraphQLClient
from .v3.nexus_v3_client import NexusV3Client


class NexusClient:
    """Lazily aggregates all synchronous Nexus Mods API clients.

    Examples:
        Access only the API versions an application needs::

            with NexusClient(auth=ApiKeyAuth.from_value(api_key)) as client:
                games = client.v1.games()
    """

    __auth: Optional[ApiKeyAuth | OAuthAuth]
    __config: NexusConfig
    __http_client: Optional[httpx.Client]
    __graphql: Optional[NexusGraphQLClient]
    __v1: Optional[NexusV1Client]
    __v3: Optional[NexusV3Client]

    def __init__(
        self,
        config: Optional[NexusConfig] = None,
        auth: Optional[ApiKeyAuth | OAuthAuth] = None,
        *,
        http_client: Optional[httpx.Client] = None,
    ) -> None:
        """Initializes an aggregate without creating any API subclient.

        Args:
            config (Optional[NexusConfig]): Shared client configuration.
            auth (Optional[ApiKeyAuth | OAuthAuth]): Optional authentication.
            http_client (Optional[httpx.Client]): Optional caller-owned client.
        """

        self.__config = config or NexusConfig()
        self.__auth = auth
        self.__http_client = http_client
        self.__v1 = None
        self.__graphql = None
        self.__v3 = None

    @property
    def v1(self) -> NexusV1Client:
        """The lazily created REST v1 client."""

        if self.__v1 is None:
            self.__v1 = NexusV1Client(
                self.__config, self.__auth, http_client=self.__http_client
            )
        return self.__v1

    @property
    def graphql(self) -> NexusGraphQLClient:
        """The lazily created GraphQL v2 client."""

        if self.__graphql is None:
            self.__graphql = NexusGraphQLClient(
                self.__config, self.__auth, http_client=self.__http_client
            )
        return self.__graphql

    @property
    def v2(self) -> NexusGraphQLClient:
        """The GraphQL v2 client under its version alias."""

        return self.graphql

    @property
    def v3(self) -> NexusV3Client:
        """The lazily created REST v3 client."""

        if self.__v3 is None:
            self.__v3 = NexusV3Client(
                self.__config, self.__auth, http_client=self.__http_client
            )
        return self.__v3

    def close(self) -> None:
        """Closes only subclients that were actually created."""

        if self.__v1 is not None:
            self.__v1.close()
        if self.__graphql is not None:
            self.__graphql.close()
        if self.__v3 is not None:
            self.__v3.close()

    def __enter__(self) -> "NexusClient":
        """Enters the synchronous aggregate context.

        Returns:
            NexusClient: This aggregate client.
        """

        return self

    def __exit__(
        self,
        exception_type: Optional[type[BaseException]],
        exception: Optional[BaseException],
        traceback: Optional[object],
    ) -> None:
        """Leaves the aggregate context and releases created resources.

        Args:
            exception_type (Optional[type[BaseException]]): Raised exception type.
            exception (Optional[BaseException]): Raised exception instance.
            traceback (Optional[object]): Raised exception traceback.
        """

        self.close()
