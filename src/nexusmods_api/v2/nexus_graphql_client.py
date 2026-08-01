"""Copyright (c) Modding Forge."""

from typing import Optional

import httpx

from ..auth.api_key_auth import ApiKeyAuth
from ..auth.oauth_auth import OAuthAuth
from ..errors.nexus_response_validation_error import NexusResponseValidationError
from ..models.rate_limit_state import RateLimitState
from ..nexus_config import NexusConfig
from ..transport.response import parse_response
from ..transport.sync_transport import SyncTransport
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
from .uid import decode_mod_uid


class NexusGraphQLClient:
    """Provides generic and convenient synchronous GraphQL v2 operations."""

    __transport: SyncTransport
    __url: str
    last_errors: tuple[GraphQLIssue, ...]

    def __init__(
        self,
        config: Optional[NexusConfig] = None,
        auth: Optional[ApiKeyAuth | OAuthAuth] = None,
        *,
        http_client: Optional[httpx.Client] = None,
    ) -> None:
        """Initializes a synchronous GraphQL v2 client."""

        resolved: NexusConfig = config or NexusConfig()
        self.__url = resolved.v2_url
        self.__transport = SyncTransport(
            resolved,
            auth,
            http_client=http_client,
        )
        self.last_errors = ()

    @property
    def rate_limits(self) -> RateLimitState:
        """Returns the latest observed GraphQL rate-limit state."""

        return self.__transport.rate_limits

    def execute[ResponseT](
        self,
        document: str,
        response_model: type[ResponseT],
        *,
        variables: Optional[dict[str, JsonValue]] = None,
        operation_name: Optional[str] = None,
        allow_partial: bool = False,
    ) -> ResponseT:
        """Executes and validates an arbitrary GraphQL document."""

        response: httpx.Response = self.__request(
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

    def execute_raw(
        self,
        document: str,
        *,
        variables: Optional[dict[str, JsonValue]] = None,
        operation_name: Optional[str] = None,
    ) -> GraphQLResponse:
        """Executes a document while preserving raw partial data and errors."""

        response: httpx.Response = self.__request(
            document,
            variables,
            operation_name,
        )
        envelope: GraphQLResponse = parse_response(response, GraphQLResponse)
        self.last_errors = tuple(envelope.errors or ())
        return envelope

    def get_games(self, *, count: int = 20, offset: int = 0) -> GraphQLPage[GraphQLGame]:
        """Returns a page of games."""

        data: dict[str, GraphQLPage[GraphQLGame]] = self.execute(
            GAMES_QUERY,
            dict[str, GraphQLPage[GraphQLGame]],
            variables={"count": count, "offset": offset},
            operation_name="Games",
        )
        return self.__root(data, "games")

    def get_mod(self, uid: str) -> GraphQLMod:
        """Returns one mod by globally unique identifier.

        Raises:
            ValueError: If the UID is not an unsigned decimal 64-bit integer.
        """

        game_id, mod_id = decode_mod_uid(uid)
        data: dict[str, GraphQLMod] = self.execute(
            MOD_QUERY,
            dict[str, GraphQLMod],
            variables={"modId": str(mod_id), "gameId": str(game_id)},
            operation_name="Mod",
        )
        return self.__root(data, "mod")

    def search_mods(
        self,
        query: str,
        *,
        count: int = 20,
        offset: int = 0,
    ) -> GraphQLPage[GraphQLMod]:
        """Searches mods and returns one typed result page."""

        data: dict[str, GraphQLPage[GraphQLMod]] = self.execute(
            SEARCH_MODS_QUERY,
            dict[str, GraphQLPage[GraphQLMod]],
            variables={
                "filter": {
                    "name": [{"value": query, "op": "WILDCARD"}],
                },
                "count": count,
                "offset": offset,
            },
            operation_name="SearchMods",
        )
        return self.__root(data, "mods")

    def get_mod_files(
        self,
        uid: str,
        *,
        count: int = 20,
        offset: int = 0,
    ) -> GraphQLPage[GraphQLModFile]:
        """Returns a typed page of files for one mod UID.

        Raises:
            ValueError: If the UID is not an unsigned decimal 64-bit integer.
        """

        game_id, mod_id = decode_mod_uid(uid)
        data: dict[str, list[GraphQLModFile]] = self.execute(
            MOD_FILES_QUERY,
            dict[str, list[GraphQLModFile]],
            variables={"modId": str(mod_id), "gameId": str(game_id)},
            operation_name="ModFiles",
        )
        files: list[GraphQLModFile] = self.__root(data, "modFiles")
        nodes: list[GraphQLModFile] = files[offset : offset + count]
        return GraphQLPage(
            nodes=nodes,
            totalCount=len(files),
            nodesCount=len(nodes),
        )

    def get_collection(
        self,
        slug: str,
        *,
        game_domain: Optional[str] = None,
    ) -> GraphQLCollection:
        """Returns one collection by slug."""

        data: dict[str, GraphQLCollection] = self.execute(
            COLLECTION_QUERY,
            dict[str, GraphQLCollection],
            variables={"slug": slug, "domainName": game_domain},
            operation_name="Collection",
        )
        return self.__root(data, "collection")

    def get_revision(
        self,
        slug: str,
        revision_number: int,
        *,
        game_domain: Optional[str] = None,
    ) -> GraphQLRevision:
        """Returns one numbered revision belonging to a collection slug."""

        data: dict[str, GraphQLRevision] = self.execute(
            REVISION_QUERY,
            dict[str, GraphQLRevision],
            variables={
                "slug": slug,
                "revision": revision_number,
                "domainName": game_domain,
            },
            operation_name="Revision",
        )
        return self.__root(data, "collectionRevision")

    def get_user(self, user_id: int) -> GraphQLUser:
        """Returns one public Nexus Mods user."""

        data: dict[str, GraphQLUser] = self.execute(
            USER_QUERY,
            dict[str, GraphQLUser],
            variables={"id": user_id},
            operation_name="User",
        )
        return self.__root(data, "user")

    def close(self) -> None:
        """Closes internally owned HTTP resources."""

        self.__transport.close()

    def __enter__(self) -> "NexusGraphQLClient":
        """Enters the synchronous client context."""

        return self

    def __exit__(
        self,
        exception_type: Optional[type[BaseException]],
        exception: Optional[BaseException],
        traceback: Optional[object],
    ) -> None:
        """Leaves the client context and releases owned resources."""

        self.close()

    def __request(
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
        return self.__transport.request(
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
