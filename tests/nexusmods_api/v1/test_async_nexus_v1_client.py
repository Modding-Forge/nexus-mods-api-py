"""Copyright (c) Modding Forge."""

import httpx

from nexusmods_api.nexus_config import NexusConfig
from nexusmods_api.v1.async_nexus_v1_client import AsyncNexusV1Client

from .payloads import response_payload


class TestAsyncNexusV1Client:
    """Tests sync/async parity for the complete REST v1 surface."""

    async def test_calls_and_validates_every_v1_route(self) -> None:
        """Tests all asynchronous query and mutation paths."""

        # given
        requests: list[httpx.Request] = []

        async def handler(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            return httpx.Response(
                200,
                json=response_payload(request.method, request.url.path),
            )

        http_client: httpx.AsyncClient = httpx.AsyncClient(
            transport=httpx.MockTransport(handler)
        )
        client: AsyncNexusV1Client = AsyncNexusV1Client(
            NexusConfig(v1_base_url="http://127.0.0.1/v1"),
            http_client=http_client,
        )

        # when / then
        assert (await client.validate_api_key()).user_id == 1
        assert (await client.get_tracked_mods())[0].mod_id == 2
        assert (await client.track_mod("game", 2)).message
        assert (await client.untrack_mod("game", 2)).message
        assert (await client.get_games())[0].id == 1
        assert (await client.get_latest_added("game"))[0].mod_id == 2
        assert (await client.get_latest_updated("game"))[0].mod_id == 2
        assert (await client.get_trending("game"))[0].mod_id == 2
        assert (await client.get_endorsements())[0].mod_id == 2
        assert (await client.get_colour_schemes())[0].id == 1
        assert (await client.get_game("game")).id == 1
        assert (await client.get_updated_mods("game", "1w"))[0].mod_id == 2
        assert (await client.get_mod("game", 2)).mod_id == 2
        assert await client.get_changelogs("game", 2)
        assert (await client.get_mod_files("game", 2)).files
        assert (await client.get_file("game", 2, 4)).file_id == 4
        assert (await client.get_download_links("game", 2, 4))[0].name == "CDN"
        assert (await client.search_file_by_md5("game", "b" * 32))[0].mod
        assert (
            await client.set_mod_endorsement("game", 2, "1.0", "abstain")
        ).message
        assert requests[-1].method == "POST"
        assert client.rate_limits.daily_remaining is None
        await client.close()
        assert http_client.is_closed is False
        await http_client.aclose()

    async def test_closes_owned_client_context(self) -> None:
        """Tests asynchronous context-managed ownership."""

        # given
        client: AsyncNexusV1Client = AsyncNexusV1Client()

        # when
        async with client:
            pass

        # then
        assert True
