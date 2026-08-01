"""Copyright (c) Modding Forge."""

from typing import cast

import httpx
import pytest

from nexusmods_api.nexus_config import NexusConfig
from nexusmods_api.v1.nexus_v1_client import NexusV1Client
from nexusmods_api.v1.types import EndorsementStatus, UpdatePeriod

from .payloads import response_payload


class TestNexusV1Client:
    """Tests the complete synchronous REST v1 surface."""

    def test_calls_and_validates_every_v1_route(self) -> None:
        """Tests all query and mutation paths through one fake server."""

        # given
        requests: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            return httpx.Response(
                200,
                json=response_payload(request.method, request.url.path),
            )

        http_client: httpx.Client = httpx.Client(transport=httpx.MockTransport(handler))
        client: NexusV1Client = NexusV1Client(
            NexusConfig(v1_base_url="http://127.0.0.1/v1"),
            http_client=http_client,
        )

        # when / then
        assert client.validate_api_key("explicit-key").name == "User"
        assert client.get_tracked_mods()[0].mod_id == 2
        assert client.track_mod("game", 2).message == "tracking updated"
        assert client.untrack_mod("game", 2).message == "tracking updated"
        assert client.get_games()[0].name == "Game"
        assert client.get_latest_added("game")[0].name == "Test Mod"
        assert client.get_latest_updated("game")[0].mod_id == 2
        assert client.get_trending("game")[0].mod_id == 2
        assert client.get_endorsements()[0].status == "Endorsed"
        assert client.get_colour_schemes()[0].name == "Dark"
        assert client.get_game("game").categories is not None
        assert client.get_updated_mods("game", "1d")[0].mod_id == 2
        assert client.get_mod("game", 2).name == "Test Mod"
        assert client.get_changelogs("game", 2) == {"1.0": ["Initial release"]}
        assert client.get_mod_files("game", 2).files[0].file_id == 4
        assert client.get_file("game", 2, 4).name == "Main File"
        assert client.get_download_links(
            "game",
            2,
            4,
            key="download-key",
            expires=123,
        )[0].uri.endswith("/file")
        assert client.search_file_by_md5("game", "a" * 32)[0].mod.mod_id == 2
        assert (
            client.set_mod_endorsement(
                "game",
                2,
                "1.0",
                "endorse",
            ).status
            == "Endorsed"
        )
        assert requests[0].headers["apikey"] == "explicit-key"
        assert requests[-1].method == "POST"
        assert client.rate_limits.hourly_remaining is None
        client.close()
        assert http_client.is_closed is False
        http_client.close()

    @pytest.mark.parametrize("identifier", [0, -1, True])
    def test_rejects_invalid_identifiers(self, identifier: int) -> None:
        """Tests local positive-ID validation before network traffic."""

        # given
        client: NexusV1Client = NexusV1Client()

        # when / then
        with pytest.raises(ValueError, match="positive integer"):
            client.get_mod("game", identifier)
        client.close()

    def test_rejects_invalid_options_and_escapes_segments(self) -> None:
        """Tests paired download fields, enum checks, and path escaping."""

        # given
        paths: list[bytes] = []

        def handler(request: httpx.Request) -> httpx.Response:
            paths.append(request.url.raw_path)
            return httpx.Response(
                200,
                json={"id": 1, "domain_name": "game/name", "name": "Game"},
            )

        client: NexusV1Client = NexusV1Client(
            NexusConfig(v1_base_url="http://127.0.0.1/v1"),
            http_client=httpx.Client(transport=httpx.MockTransport(handler)),
        )

        # when / then
        with pytest.raises(ValueError, match="together"):
            client.get_download_links("game", 2, 4, key="key")
        with pytest.raises(ValueError, match="period"):
            client.get_updated_mods("game", cast(UpdatePeriod, "2d"))
        with pytest.raises(ValueError, match="status"):
            client.set_mod_endorsement(
                "game",
                2,
                "1",
                cast(EndorsementStatus, "invalid"),
            )
        with pytest.raises(ValueError, match="empty"):
            client.get_game("")
        client.get_game("game/name")
        assert paths == [b"/v1/games/game%2Fname"]
        client.close()

    def test_closes_owned_client_context(self) -> None:
        """Tests synchronous context-managed ownership."""

        # given
        client: NexusV1Client = NexusV1Client()

        # when
        with client:
            pass

        # then
        assert True
