"""Copyright (c) Modding Forge."""

import inspect
import re
from collections.abc import Callable, Coroutine
from typing import cast

import httpx

from nexusmods_api.nexus_config import NexusConfig
from nexusmods_api.types import JsonValue
from nexusmods_api.v3.async_nexus_v3_client import AsyncNexusV3Client
from nexusmods_api.v3.generated.operations import OPERATIONS


class TestAsyncNexusV3Client:
    """Tests sync/async parity across all generated REST v3 operations."""

    async def test_invokes_every_generated_operation(self) -> None:
        """Tests every asynchronous generated method and generic response path."""

        # given
        requests: list[httpx.Request] = []

        async def handler(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            return httpx.Response(200, json={"ok": True})

        http_client: httpx.AsyncClient = httpx.AsyncClient(
            transport=httpx.MockTransport(handler)
        )
        client: AsyncNexusV3Client = AsyncNexusV3Client(
            NexusConfig(
                v3_base_url="http://127.0.0.1/v3",
                warn_on_unstable=False,
            ),
            http_client=http_client,
        )

        # when
        for operation in OPERATIONS.values():
            method = cast(
                Callable[..., Coroutine[None, None, JsonValue]],
                getattr(client, self.__method_name(operation.operation_id)),
            )
            signature: inspect.Signature = inspect.signature(method)
            arguments: dict[str, object] = {
                name: 1
                for name, parameter in signature.parameters.items()
                if parameter.default is inspect.Parameter.empty
            }
            arguments["query"] = {"preview": True}
            if operation.has_body:
                arguments["body"] = {"name": "value"}
            assert await method(**arguments) == {"ok": True}

        # then
        assert len(requests) == len(OPERATIONS)
        assert len(client.operations) == len(OPERATIONS)
        assert client.rate_limits.hourly_remaining is None
        assert await client.request(
            "getGameDlcs",
            dict[str, bool],
            path_parameters={"game_domain": "game"},
        ) == {"ok": True}
        await client.close()
        assert http_client.is_closed is False
        await http_client.aclose()

    async def test_handles_no_content_and_owned_context(self) -> None:
        """Tests asynchronous 204 handling and context cleanup."""

        # given
        async def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(204)

        client: AsyncNexusV3Client = AsyncNexusV3Client(
            NexusConfig(
                v3_base_url="http://127.0.0.1/v3",
                warn_on_unstable=False,
            ),
            http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
        )

        # when / then
        assert await client.edit_collection(1, body={}) is None
        await client.close()
        async with AsyncNexusV3Client():
            pass

    @staticmethod
    def __method_name(operation_id: str) -> str:
        """Converts an operation ID to its generated method name."""

        return re.sub(r"(?<!^)(?=[A-Z])", "_", operation_id).lower()
