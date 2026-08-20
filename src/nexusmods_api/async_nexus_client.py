"""Copyright (c) Modding Forge."""

from typing import Optional

import httpx

from .auth.api_key_auth import ApiKeyAuth
from .auth.async_oauth_auth import AsyncOAuthAuth
from .nexus_config import NexusConfig
from .v1.async_nexus_v1_client import AsyncNexusV1Client
from .v2.async_nexus_graphql_client import AsyncNexusGraphQLClient
from .v3.async_nexus_v3_client import AsyncNexusV3Client


class AsyncNexusClient:
    """Lazily aggregates all asynchronous Nexus Mods API clients.

    Examples:
        Access only the API versions an application needs::

            async with AsyncNexusClient(
                auth=ApiKeyAuth.from_value(api_key)
            ) as client:
                games = await client.v1.games()
    """

    __auth: Optional[ApiKeyAuth | AsyncOAuthAuth]
    __config: NexusConfig
    __http_client: Optional[httpx.AsyncClient]
    __graphql: Optional[AsyncNexusGraphQLClient]
    __v1: Optional[AsyncNexusV1Client]
    __v3: Optional[AsyncNexusV3Client]

    def __init__(
        self,
        config: Optional[NexusConfig] = None,
        auth: Optional[ApiKeyAuth | AsyncOAuthAuth] = None,
        *,
        http_client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        """Initializes an aggregate without creating any API subclient.

        Args:
            config (Optional[NexusConfig]): Shared client configuration.
            auth (Optional[ApiKeyAuth | AsyncOAuthAuth]): Optional authentication.
            http_client (Optional[httpx.AsyncClient]): Optional caller-owned client.
        """

        self.__config = config or NexusConfig()
        self.__auth = auth
        self.__http_client = http_client
        self.__v1 = None
        self.__graphql = None
        self.__v3 = None

    @property
    def v1(self) -> AsyncNexusV1Client:
        """The lazily created REST v1 client."""

        if self.__v1 is None:
            self.__v1 = AsyncNexusV1Client(
                self.__config, self.__auth, http_client=self.__http_client
            )
        return self.__v1

    @property
    def graphql(self) -> AsyncNexusGraphQLClient:
        """The lazily created GraphQL v2 client."""

        if self.__graphql is None:
            self.__graphql = AsyncNexusGraphQLClient(
                self.__config, self.__auth, http_client=self.__http_client
            )
        return self.__graphql

    @property
    def v2(self) -> AsyncNexusGraphQLClient:
        """The GraphQL v2 client under its version alias."""

        return self.graphql

    @property
    def v3(self) -> AsyncNexusV3Client:
        """The lazily created REST v3 client."""

        if self.__v3 is None:
            self.__v3 = AsyncNexusV3Client(
                self.__config, self.__auth, http_client=self.__http_client
            )
        return self.__v3

    async def close(self) -> None:
        """Closes only subclients that were actually created."""

        if self.__v1 is not None:
            await self.__v1.close()
        if self.__graphql is not None:
            await self.__graphql.close()
        if self.__v3 is not None:
            await self.__v3.close()

    async def __aenter__(self) -> "AsyncNexusClient":
        """Enters the asynchronous aggregate context.

        Returns:
            AsyncNexusClient: This aggregate client.
        """

        return self

    async def __aexit__(
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

        await self.close()
