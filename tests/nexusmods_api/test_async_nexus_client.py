"""Copyright (c) Modding Forge."""

import json
from typing import cast

import httpx

from nexusmods_api import AsyncNexusClient, NexusConfig
from nexusmods_api.types import JsonValue

from .v1.payloads import response_payload
from .v2.payloads import operation_payload


class TestAsyncNexusClient:
    """Tests the lazy asynchronous aggregate."""

    async def test_lazily_exposes_all_api_clients(self) -> None:
        """Tests stable identity and requests through every async API property."""

        # given
        async def handler(request: httpx.Request) -> httpx.Response:
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

        http_client: httpx.AsyncClient = httpx.AsyncClient(
            transport=httpx.MockTransport(handler)
        )
        client: AsyncNexusClient = AsyncNexusClient(
            NexusConfig(
                v1_base_url="http://127.0.0.1/v1",
                v2_url="http://127.0.0.1/graphql",
                v3_base_url="http://127.0.0.1/v3",
                warn_on_unstable=False,
            ),
            http_client=http_client,
        )

        # when / then
        assert (await client.v1.get_games())[0].id == 1
        assert (await client.v2.get_games()).nodes[0].id == 1
        assert client.graphql is client.v2
        assert client.v1 is client.v1
        assert await client.v3.get_game_dlcs("game") == []
        assert client.v3 is client.v3
        await client.close()
        assert http_client.is_closed is False
        await http_client.aclose()

    async def test_closes_empty_owned_context(self) -> None:
        """Tests lazy asynchronous no-op cleanup."""

        # given / when / then
        async with AsyncNexusClient():
            pass
