"""Copyright (c) Modding Forge."""

import json
from typing import cast

import httpx

from nexusmods_api.nexus_config import NexusConfig
from nexusmods_api.types import JsonValue
from nexusmods_api.v2.async_nexus_graphql_client import AsyncNexusGraphQLClient

from .payloads import operation_payload


class TestAsyncNexusGraphQLClient:
    """Tests sync/async parity for GraphQL v2."""

    async def test_executes_all_convenience_queries_and_raw(self) -> None:
        """Tests all asynchronous typed convenience operations."""

        # given
        async def handler(request: httpx.Request) -> httpx.Response:
            payload: dict[str, JsonValue] = cast(
                dict[str, JsonValue],
                json.loads(request.content),
            )
            operation_name: JsonValue = payload.get("operationName")
            return httpx.Response(
                200,
                json=operation_payload(
                    operation_name if isinstance(operation_name, str) else None
                ),
            )

        http_client: httpx.AsyncClient = httpx.AsyncClient(
            transport=httpx.MockTransport(handler)
        )
        client: AsyncNexusGraphQLClient = AsyncNexusGraphQLClient(
            NexusConfig(v2_url="http://127.0.0.1/graphql"),
            http_client=http_client,
        )

        # when / then
        assert (await client.get_games()).nodes[0].id == 1
        assert (await client.get_mod("4294967298")).uid == "4294967298"
        assert (await client.search_mods("Mod")).total_count == 1
        assert (await client.get_mod_files("4294967298")).nodes[0].uid
        assert (await client.get_collection("collection")).slug == "collection"
        assert (await client.get_revision("collection", 1)).id == 5
        assert (await client.get_user(6)).name == "User"
        raw = await client.execute_raw("query { answer }")
        assert raw.data == {"answer": 42}
        assert client.rate_limits.hourly_remaining is None
        await client.close()
        assert http_client.is_closed is False
        await http_client.aclose()

    async def test_closes_owned_context(self) -> None:
        """Tests asynchronous context-managed cleanup."""

        # given / when / then
        async with AsyncNexusGraphQLClient():
            pass
