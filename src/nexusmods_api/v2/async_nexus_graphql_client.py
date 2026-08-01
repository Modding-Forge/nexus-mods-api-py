"""Copyright (c) Modding Forge."""

from typing import Optional

import httpx

from ..auth.api_key_auth import ApiKeyAuth
from ..auth.async_oauth_auth import AsyncOAuthAuth
from ..errors.nexus_response_validation_error import NexusResponseValidationError
from ..models.rate_limit_state import RateLimitState
from ..nexus_config import NexusConfig
from ..transport.async_transport import AsyncTransport
from ..transport.response import parse_response
from ..types import JsonValue
from .executor import parse_graphql_data
from .models.graphql_collection import GraphQLCollection
from .models.graphql_game import GraphQLGame
from .models.graphql_issue import GraphQLIssue
from .models.graphql_mod import GraphQLMod
from .models.graphql_mod_file import GraphQLModFile
from .models.graphql_page import GraphQLPage
from .models.graphql_response import GraphQLResponse
from .models.graphql_revision import GraphQLRevision
from .models.graphql_user import GraphQLUser
from .operations import (
    COLLECTION_QUERY,
    GAMES_QUERY,
    MOD_FILES_QUERY,
    MOD_QUERY,
    REVISION_QUERY,
    SEARCH_MODS_QUERY,
    USER_QUERY,
)


class AsyncNexusGraphQLClient:
    """Provides generic and convenient asynchronous GraphQL v2 operations."""

    __transport: AsyncTransport
    __url: str
    last_errors: tuple[GraphQLIssue, ...]

    def __init__(
        self,
        config: Optional[NexusConfig] = None,
        auth: Optional[ApiKeyAuth | AsyncOAuthAuth] = None,
        *,
        http_client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        """Initializes an asynchronous GraphQL v2 client."""

        resolved: NexusConfig = config or NexusConfig()
        self.__url = resolved.v2_url
        self.__transport = AsyncTransport(
            resolved,
            auth,
            http_client=http_client,
        )
        self.last_errors = ()

    @property
    def rate_limits(self) -> RateLimitState:
        """Returns the latest observed GraphQL rate-limit state."""

        return self.__transport.rate_limits

    async def execute[ResponseT](
        self,
        document: str,
        response_model: type[ResponseT],
        *,
        variables: Optional[dict[str, JsonValue]] = None,
        operation_name: Optional[str] = None,
        allow_partial: bool = False,
    ) -> ResponseT:
        """Executes and validates an arbitrary GraphQL document."""

        response: httpx.Response = await self.__request(
            document,
            variables,
            operation_name,
        )
        data, issues = parse_graphql_data(
            response,
            response_model,
            allow_partial=allow_partial,
        )
        self.last_errors = issues
        return data

    async def execute_raw(
        self,
        document: str,
        *,
        variables: Optional[dict[str, JsonValue]] = None,
        operation_name: Optional[str] = None,
    ) -> GraphQLResponse:
        """Executes a document while preserving raw partial data and errors."""

        response: httpx.Response = await self.__request(
            document,
            variables,
            operation_name,
        )
        envelope: GraphQLResponse = parse_response(response, GraphQLResponse)
        self.last_errors = tuple(envelope.errors or ())
        return envelope

    async def get_games(
        self,
        *,
        count: int = 20,
        offset: int = 0,
    ) -> GraphQLPage[GraphQLGame]:
        """Returns a page of games."""

        data: dict[str, GraphQLPage[GraphQLGame]] = await self.execute(
            GAMES_QUERY,
            dict[str, GraphQLPage[GraphQLGame]],
            variables={"count": count, "offset": offset},
            operation_name="Games",
        )
        return self.__root(data, "games")

    async def get_mod(self, uid: str) -> GraphQLMod:
        """Returns one mod by globally unique identifier."""

        data: dict[str, GraphQLMod] = await self.execute(
            MOD_QUERY,
            dict[str, GraphQLMod],
            variables={"uid": uid},
            operation_name="Mod",
        )
        return self.__root(data, "mod")

    async def search_mods(
        self,
        query: str,
        *,
        count: int = 20,
        offset: int = 0,
    ) -> GraphQLPage[GraphQLMod]:
        """Searches mods and returns one typed result page."""

        data: dict[str, GraphQLPage[GraphQLMod]] = await self.execute(
            SEARCH_MODS_QUERY,
            dict[str, GraphQLPage[GraphQLMod]],
            variables={"query": query, "count": count, "offset": offset},
            operation_name="SearchMods",
        )
        return self.__root(data, "mods")

    async def get_mod_files(
        self,
        uid: str,
        *,
        count: int = 20,
        offset: int = 0,
    ) -> GraphQLPage[GraphQLModFile]:
        """Returns a typed page of files for one mod UID."""

        data: dict[str, GraphQLPage[GraphQLModFile]] = await self.execute(
            MOD_FILES_QUERY,
            dict[str, GraphQLPage[GraphQLModFile]],
            variables={"uid": uid, "count": count, "offset": offset},
            operation_name="ModFiles",
        )
        return self.__root(data, "modFiles")

    async def get_collection(self, slug: str) -> GraphQLCollection:
        """Returns one collection by slug."""

        data: dict[str, GraphQLCollection] = await self.execute(
            COLLECTION_QUERY,
            dict[str, GraphQLCollection],
            variables={"slug": slug},
            operation_name="Collection",
        )
        return self.__root(data, "collection")

    async def get_revision(self, revision_id: int) -> GraphQLRevision:
        """Returns one collection revision by numeric identifier."""

        data: dict[str, GraphQLRevision] = await self.execute(
            REVISION_QUERY,
            dict[str, GraphQLRevision],
            variables={"id": revision_id},
            operation_name="Revision",
        )
        return self.__root(data, "collectionRevision")

    async def get_user(self, user_id: int) -> GraphQLUser:
        """Returns one public Nexus Mods user."""

        data: dict[str, GraphQLUser] = await self.execute(
            USER_QUERY,
            dict[str, GraphQLUser],
            variables={"id": user_id},
            operation_name="User",
        )
        return self.__root(data, "user")

    async def close(self) -> None:
        """Closes internally owned HTTP resources."""

        await self.__transport.close()

    async def __aenter__(self) -> "AsyncNexusGraphQLClient":
        """Enters the asynchronous client context."""

        return self

    async def __aexit__(
        self,
        exception_type: Optional[type[BaseException]],
        exception: Optional[BaseException],
        traceback: Optional[object],
    ) -> None:
        """Leaves the async client context and releases owned resources."""

        await self.close()

    async def __request(
        self,
        document: str,
        variables: Optional[dict[str, JsonValue]],
        operation_name: Optional[str],
    ) -> httpx.Response:
        """Sends one retry-safe GraphQL query request."""

        payload: dict[str, JsonValue] = {
            "query": document,
            "variables": variables or {},
        }
        if operation_name is not None:
            payload["operationName"] = operation_name
        return await self.__transport.request(
            "POST",
            self.__url,
            json=payload,
            retry_safe=True,
        )

    @staticmethod
    def __root[ResponseT](data: dict[str, ResponseT], name: str) -> ResponseT:
        """Returns a required convenience-query root field."""

        try:
            return data[name]
        except KeyError as error:
            raise NexusResponseValidationError(
                f"The GraphQL response omitted the {name} field."
            ) from error
