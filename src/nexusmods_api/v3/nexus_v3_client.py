"""Copyright (c) Modding Forge."""

from typing import Optional, TypeVar
from urllib.parse import quote

import httpx

from ..auth.api_key_auth import ApiKeyAuth
from ..auth.oauth_auth import OAuthAuth
from ..models.rate_limit_state import RateLimitState
from ..nexus_config import NexusConfig
from ..transport.response import parse_json_response, parse_response
from ..transport.sync_transport import SyncTransport
from ..types import JsonValue, QueryParameters
from .generated.operations import OPERATIONS
from .generated.sync_operations import GeneratedSyncOperations
from .stability import warn_if_unstable
from .v3_operation import V3Operation

ResponseT = TypeVar("ResponseT")


class NexusV3Client(GeneratedSyncOperations):
    """Provides generated synchronous access to every pinned REST v3 operation.

    Examples:
        Use a generated method or the typed generic executor::

            game = client.get_game("skyrimspecialedition")
            result = client.request("getGame", Game, path_parameters={
                "game_domain": "skyrimspecialedition",
            })
    """

    __base_url: str
    __transport: SyncTransport
    __warn_on_unstable: bool

    def __init__(
        self,
        config: Optional[NexusConfig] = None,
        auth: Optional[ApiKeyAuth | OAuthAuth] = None,
        *,
        http_client: Optional[httpx.Client] = None,
    ) -> None:
        """Initializes a synchronous REST v3 client.

        Args:
            config (Optional[NexusConfig]): Shared client configuration.
            auth (Optional[ApiKeyAuth | OAuthAuth]): Optional authentication.
            http_client (Optional[httpx.Client]): Optional caller-owned HTTP client.
        """

        resolved: NexusConfig = config or NexusConfig()
        self.__base_url = resolved.v3_base_url
        self.__warn_on_unstable = resolved.warn_on_unstable
        self.__transport = SyncTransport(
            resolved,
            auth,
            http_client=http_client,
        )

    @property
    def rate_limits(self) -> RateLimitState:
        """The latest observed REST v3 rate-limit state."""

        return self.__transport.rate_limits

    @property
    def operations(self) -> dict[str, V3Operation]:
        """A defensive copy of the generated operation registry."""

        return dict(OPERATIONS)

    def request(
        self,
        operation_id: str,
        response_model: type[ResponseT],
        *,
        path_parameters: Optional[dict[str, str | int | float | bool]] = None,
        query: Optional[QueryParameters] = None,
        body: JsonValue = None,
    ) -> ResponseT:
        """Executes one generated operation and validates a caller-selected model.

        Args:
            operation_id (str): Stable OpenAPI operation identifier.
            response_model (type[ResponseT]): Expected response type.
            path_parameters (Optional[dict[str, str | int | float | bool]]):
                Values for every path placeholder.
            query (Optional[QueryParameters]): Optional query parameters.
            body (JsonValue): Optional JSON request body.

        Returns:
            ResponseT: Validated response value.

        Raises:
            ValueError: If the operation or path parameters are invalid.
            NexusResponseValidationError: If response validation fails.
        """

        response: httpx.Response = self.__send(
            operation_id,
            path_parameters or {},
            query=query,
            body=body,
        )
        return parse_response(response, response_model)

    def request_json(
        self,
        operation_id: str,
        *,
        path_parameters: Optional[dict[str, str | int | float | bool]] = None,
        query: Optional[QueryParameters] = None,
        body: JsonValue = None,
    ) -> JsonValue:
        """Executes one generated operation and returns recursive JSON data.

        Args:
            operation_id (str): Stable OpenAPI operation identifier.
            path_parameters (Optional[dict[str, str | int | float | bool]]):
                Values for every path placeholder.
            query (Optional[QueryParameters]): Optional query parameters.
            body (JsonValue): Optional JSON request body.

        Returns:
            JsonValue: Validated JSON, or `None` for an empty response body.

        Raises:
            ValueError: If the operation or path parameters are invalid.
            NexusResponseValidationError: If JSON validation fails.
        """

        response: httpx.Response = self.__send(
            operation_id,
            path_parameters or {},
            query=query,
            body=body,
        )
        if not response.content:
            return None
        return parse_json_response(response)

    def close(self) -> None:
        """Closes internally owned HTTP resources."""

        self.__transport.close()

    def __enter__(self) -> "NexusV3Client":
        """Enters the synchronous client context.

        Returns:
            NexusV3Client: This open REST v3 client.
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

    def _request_generated(
        self,
        operation_id: str,
        path_parameters: dict[str, str | int | float | bool],
        *,
        query: Optional[QueryParameters] = None,
        body: JsonValue = None,
    ) -> JsonValue:
        """Executes one explicit generated operation method.

        Args:
            operation_id (str): Stable OpenAPI operation identifier.
            path_parameters (dict[str, str | int | float | bool]): Path values.
            query (Optional[QueryParameters]): Optional query parameters.
            body (JsonValue): Optional JSON request body.

        Returns:
            JsonValue: Validated JSON, or `None` for an empty response body.
        """

        return self.request_json(
            operation_id,
            path_parameters=path_parameters,
            query=query,
            body=body,
        )

    def __send(
        self,
        operation_id: str,
        path_parameters: dict[str, str | int | float | bool],
        *,
        query: Optional[QueryParameters],
        body: JsonValue,
    ) -> httpx.Response:
        """Builds and sends one registered OpenAPI operation.

        Args:
            operation_id (str): Stable OpenAPI operation identifier.
            path_parameters (dict[str, str | int | float | bool]): Path values.
            query (Optional[QueryParameters]): Optional query parameters.
            body (JsonValue): Optional JSON request body.

        Returns:
            httpx.Response: Successful raw HTTP response.

        Raises:
            ValueError: If the operation or exact path parameters are invalid.
        """

        try:
            operation: V3Operation = OPERATIONS[operation_id]
        except KeyError as error:
            raise ValueError(f"Unknown REST v3 operation: {operation_id}.") from error
        expected: set[str] = set(operation.path_parameters)
        supplied: set[str] = set(path_parameters)
        if supplied != expected:
            missing: set[str] = expected - supplied
            extra: set[str] = supplied - expected
            raise ValueError(
                "Invalid path parameters; "
                f"missing={sorted(missing)}, extra={sorted(extra)}."
            )
        path: str = operation.path
        for name, value in path_parameters.items():
            path = path.replace(f"{{{name}}}", quote(str(value), safe=""))
        warn_if_unstable(operation, enabled=self.__warn_on_unstable)
        return self.__transport.request(
            operation.method,
            f"{self.__base_url}{path}",
            params=query,
            json=body,
            retry_safe=operation.method == "GET",
        )
