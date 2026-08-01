"""Copyright (c) Modding Forge."""

from typing import Optional
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


class NexusV3Client(GeneratedSyncOperations):
    """Provides generated synchronous access to every pinned REST v3 operation."""

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
        """Initializes a synchronous REST v3 client."""

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
        """Returns the latest observed REST v3 rate-limit state."""

        return self.__transport.rate_limits

    @property
    def operations(self) -> dict[str, V3Operation]:
        """Returns a defensive copy of the generated operation registry."""

        return dict(OPERATIONS)

    def request[ResponseT](
        self,
        operation_id: str,
        response_model: type[ResponseT],
        *,
        path_parameters: Optional[dict[str, str | int | float | bool]] = None,
        query: Optional[QueryParameters] = None,
        body: JsonValue = None,
    ) -> ResponseT:
        """Executes one generated operation and validates a caller-selected model."""

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
        """Executes one generated operation and returns recursive JSON data."""

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

    def _request_generated(
        self,
        operation_id: str,
        path_parameters: dict[str, str | int | float | bool],
        *,
        query: Optional[QueryParameters] = None,
        body: JsonValue = None,
    ) -> JsonValue:
        """Executes one explicit generated operation method."""

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
        """Builds and sends one registered OpenAPI operation."""

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
