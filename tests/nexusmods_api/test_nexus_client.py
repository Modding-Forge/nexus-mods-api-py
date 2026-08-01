"""Copyright (c) Modding Forge."""

import json
from typing import cast

import httpx

import nexusmods_api
from nexusmods_api import ApiKeyAuth, NexusClient, NexusConfig
from nexusmods_api.types import JsonValue

from .v1.payloads import response_payload
from .v2.payloads import operation_payload


class TestNexusClient:
    """Tests the lazy synchronous aggregate and public imports."""

    def test_lazily_exposes_all_api_clients(self) -> None:
        """Tests stable identity and requests through every API property."""

        # given
        def handler(request: httpx.Request) -> httpx.Response:
            if request.url.path == "/v1/games":
                return httpx.Response(
                    200,
                    json=response_payload(request.method, request.url.path),
                )
            if request.url.path == "/graphql":
                payload: dict[str, JsonValue] = cast(
                    dict[str, JsonValue],
                    json.loads(request.content),
                )
                operation: JsonValue = payload.get("operationName")
                return httpx.Response(
                    200,
                    json=operation_payload(
                        operation if isinstance(operation, str) else None
                    ),
                )
            return httpx.Response(200, json=[])

        http_client: httpx.Client = httpx.Client(transport=httpx.MockTransport(handler))
        client: NexusClient = NexusClient(
            NexusConfig(
                v1_base_url="http://127.0.0.1/v1",
                v2_url="http://127.0.0.1/graphql",
                v3_base_url="http://127.0.0.1/v3",
                warn_on_unstable=False,
            ),
            ApiKeyAuth.from_value("key"),
            http_client=http_client,
        )

        # when / then
        assert client.v1.get_games()[0].id == 1
        assert client.v2.get_games().nodes[0].id == 1
        assert client.graphql is client.v2
        assert client.v1 is client.v1
        assert client.v3.get_game_dlcs("game") == []
        assert client.v3 is client.v3
        client.close()
        assert http_client.is_closed is False
        http_client.close()

    def test_closes_empty_owned_context_and_exports_public_api(self) -> None:
        """Tests lazy no-op cleanup and the package landing import surface."""

        # given / when
        with NexusClient():
            pass

        # then
        assert nexusmods_api.__version__ == "1.0.0"
        assert "NexusV1Client" in nexusmods_api.__all__
        assert "OAuthCallbackPages" in nexusmods_api.__all__
        assert "SSOFlow" not in nexusmods_api.__all__
