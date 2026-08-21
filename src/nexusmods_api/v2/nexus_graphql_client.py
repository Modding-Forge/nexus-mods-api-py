"""Copyright (c) Modding Forge."""

from typing import Optional, TypeVar

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

ResponseT = TypeVar("ResponseT")


class NexusGraphQLClient:
    """Provides generic and convenient synchronous GraphQL v2 operations.

    Examples:
        Preserve partial data from an application-defined query::

            data = client.execute(
                document,
                dict[str, JsonValue],
                allow_partial=True,
            )
            issues = client.last_errors
    """

    __transport: SyncTransport
    __url: str
    last_errors: tuple[GraphQLIssue, ...]
    """The issues returned by the most recent GraphQL operation."""

    def __init__(
        self,
        config: Optional[NexusConfig] = None,
        auth: Optional[ApiKeyAuth | OAuthAuth] = None,
        *,
        http_client: Optional[httpx.Client] = None,
    ) -> None:
        """Initializes a synchronous GraphQL v2 client.

        Args:
            config (Optional[NexusConfig]): Shared client configuration.
            auth (Optional[ApiKeyAuth | OAuthAuth]): Optional authentication.
            http_client (Optional[httpx.Client]): Optional caller-owned HTTP client.
        """

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
        """The latest observed GraphQL rate-limit state."""

        return self.__transport.rate_limits

    def execute(
        self,
        document: str,
        response_model: type[ResponseT],
        *,
        variables: Optional[dict[str, JsonValue]] = None,
        operation_name: Optional[str] = None,
        allow_partial: bool = False,
    ) -> ResponseT:
        """Executes and validates an arbitrary GraphQL document.

        Original API documentation: https://graphql.nexusmods.com/#introduction

        Args:
            document (str): GraphQL query or mutation document.
            response_model (type[ResponseT]): Expected type of the `data` value.
            variables (Optional[dict[str, JsonValue]]): Operation variables.
            operation_name (Optional[str]): Named operation to execute.
            allow_partial (bool): Whether data may be returned alongside issues.

        Returns:
            ResponseT: Validated GraphQL data.

        Raises:
            NexusGraphQLError: If issues exist and partial data is not allowed.
            NexusResponseValidationError: If the response data cannot be validated.
        """

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
        """Executes a document while preserving raw partial data and errors.

        Original API documentation: https://graphql.nexusmods.com/#introduction

        Args:
            document (str): GraphQL query or mutation document.
            variables (Optional[dict[str, JsonValue]]): Operation variables.
            operation_name (Optional[str]): Named operation to execute.

        Returns:
            GraphQLResponse: Raw validated envelope with data and issues intact.

        Raises:
            NexusResponseValidationError: If the response is not a valid envelope.
        """

        response: httpx.Response = self.__request(
            document,
            variables,
            operation_name,
        )
        envelope: GraphQLResponse = parse_response(response, GraphQLResponse)
        self.last_errors = tuple(envelope.errors or ())
        return envelope

    def get_games(self, *, count: int = 20, offset: int = 0) -> GraphQLPage[GraphQLGame]:
        """Returns a page of games.

        Original API documentation: https://graphql.nexusmods.com/#query-games

        Args:
            count (int): Maximum number of games requested.
            offset (int): Zero-based result offset.

        Returns:
            GraphQLPage[GraphQLGame]: Requested page and total result count.
        """

        data: dict[str, GraphQLPage[GraphQLGame]] = self.execute(
            GAMES_QUERY,
            dict[str, GraphQLPage[GraphQLGame]],
            variables={"count": count, "offset": offset},
            operation_name="Games",
        )
        return self.__root(data, "games")

    def get_mod(self, uid: str) -> GraphQLMod:
        """Returns one mod by globally unique identifier.

        Original API documentation: https://graphql.nexusmods.com/#query-mod

        Args:
            uid (str): Unsigned decimal 64-bit mod UID.

        Returns:
            GraphQLMod: Matching mod metadata.

        Raises:
            ValueError: If the UID is not an unsigned decimal 64-bit integer.
            NexusResponseValidationError: If the response omits the `mod` root.
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
        """Searches mods and returns one typed result page.

        Original API documentation: https://graphql.nexusmods.com/#query-mods

        Args:
            query (str): Name search pattern passed to Nexus Mods.
            count (int): Maximum number of mods requested.
            offset (int): Zero-based result offset.

        Returns:
            GraphQLPage[GraphQLMod]: Matching mod page.
        """

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

        Original API documentation: https://graphql.nexusmods.com/#query-modFiles

        Args:
            uid (str): Unsigned decimal 64-bit mod UID.
            count (int): Maximum number of files in the local result slice.
            offset (int): Zero-based local slice offset.

        Returns:
            GraphQLPage[GraphQLModFile]: Locally sliced file page.

        Raises:
            ValueError: If the UID is not an unsigned decimal 64-bit integer.
            NexusResponseValidationError: If the response omits `modFiles`.
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
        """Returns one collection by slug.

        Original API documentation: https://graphql.nexusmods.com/#query-collection

        Args:
            slug (str): Nexus Mods collection slug.
            game_domain (Optional[str]): Game domain used to disambiguate the slug.

        Returns:
            GraphQLCollection: Matching collection metadata.

        Raises:
            NexusResponseValidationError: If the response omits `collection`.
        """

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
        """Returns one numbered revision belonging to a collection slug.

        Original API documentation: https://graphql.nexusmods.com/#query-collectionRevision

        Args:
            slug (str): Nexus Mods collection slug.
            revision_number (int): Collection revision number.
            game_domain (Optional[str]): Game domain used to disambiguate the slug.

        Returns:
            GraphQLRevision: Matching collection revision.

        Raises:
            NexusResponseValidationError: If the response omits the revision root.
        """

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
        """Returns one public Nexus Mods user.

        Original API documentation: https://graphql.nexusmods.com/#query-user

        Args:
            user_id (int): Nexus Mods member identifier.

        Returns:
            GraphQLUser: Matching public user metadata.

        Raises:
            NexusResponseValidationError: If the response omits the `user` root.
        """

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
        """Enters the synchronous client context.

        Returns:
            NexusGraphQLClient: This open GraphQL client.
        """

        return self

    def __exit__(
        self,
        exception_type: Optional[type[BaseException]],
        exception: Optional[BaseException],
        traceback: Optional[object],
    ) -> None:
        """Leaves the client context and releases owned resources.

        Args:
            exception_type (Optional[type[BaseException]]): Raised exception type.
            exception (Optional[BaseException]): Raised exception instance.
            traceback (Optional[object]): Raised exception traceback.
        """

        self.close()

    def __request(
        self,
        document: str,
        variables: Optional[dict[str, JsonValue]],
        operation_name: Optional[str],
    ) -> httpx.Response:
        """Sends one retry-safe GraphQL query request.

        Args:
            document (str): GraphQL document.
            variables (Optional[dict[str, JsonValue]]): Operation variables.
            operation_name (Optional[str]): Named operation to execute.

        Returns:
            httpx.Response: Successful raw HTTP response.
        """

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
    def __root(data: dict[str, ResponseT], name: str) -> ResponseT:
        """Returns a required convenience-query root field.

        Args:
            data (dict[str, ResponseT]): Validated GraphQL data mapping.
            name (str): Required root field name.

        Returns:
            ResponseT: Value stored under `name`.

        Raises:
            NexusResponseValidationError: If the root field is absent.
        """

        try:
            return data[name]
        except KeyError as error:
            raise NexusResponseValidationError(
                f"The GraphQL response omitted the {name} field."
            ) from error
