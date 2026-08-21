"""Copyright (c) Modding Forge."""

import inspect
from datetime import UTC, datetime
from typing import cast

import httpx
import pytest

from nexusmods_api.nexus_config import NexusConfig
from nexusmods_api.v1.async_nexus_v1_client import AsyncNexusV1Client
from nexusmods_api.v1.models.endorsement import Endorsement
from nexusmods_api.v1.nexus_v1_client import NexusV1Client
from nexusmods_api.v1.types import EndorsementStatus, UpdatePeriod

from .payloads import response_payload


class TestNexusV1Client:
    """Tests the complete synchronous REST v1 surface."""

    def test_endpoint_docstrings_link_official_operations(self) -> None:
        """Tests Swagger operation links and sync/async documentation parity."""

        # given
        base_url: str = (
            "https://app.swaggerhub.com/apis-docs/NexusMods/"
            "nexus-mods_public_api_params_in_form_data/1.0"
        )
        suffixes: dict[str, tuple[str, ...]] = {
            "validate_api_key": ("#/User/post_v1_users_validate.json",),
            "get_tracked_mods": ("#/User/get_v1_user_tracked_mods.json",),
            "track_mod": ("#/User/post_v1_user_tracked_mods.json",),
            "untrack_mod": ("#/User/delete_v1_user_tracked_mods.json",),
            "get_games": ("#/Games/get_v1_games.json",),
            "get_latest_added": (
                "#/Mods/get_v1_games_game_domain_mods_latest_added.json",
            ),
            "get_latest_updated": ("#/Mods",),
            "get_trending": ("#/Mods/get_v1_games_game_domain_mods_trending.json",),
            "get_endorsements": ("#/User/get_v1_user_endorsements.json",),
            "get_colour_schemes": ("#/Colour%20Schemes/get_v1_colourschemes.json",),
            "get_game": ("#/Games/get_v1_games_game_domain.json",),
            "get_updated_mods": ("#/Mods/get_v1_games_game_domain_mods_updates.json",),
            "get_mod": ("#/Mods/get_v1_games_game_domain_name_mods_id.json",),
            "get_changelogs": (
                "#/Mods/get_v1_games_game_domain_mods_mod_id_changelogs.json",
            ),
            "get_mod_files": (
                "#/Mod%20Files/get_v1_games_game_domain_mods_mod_id_files.json",
            ),
            "get_file": (
                "#/Mod%20Files/get_v1_games_game_domain_mods_mod_id_files_file_id.json",
            ),
            "get_download_links": (
                "#/Mod%20Files/"
                "get_v1_games_game_domain_mods_mod_id_files_id_download_link.json",
            ),
            "search_file_by_md5": (
                "#/Mods/get_v1_games_game_domain_name_mods_md5_search_md5_hash.json",
            ),
            "set_mod_endorsement": (
                "#/Mods/post_v1_games_game_domain_name_mods_id_endorse.json",
                "#/Mods/post_v1_games_game_domain_name_mods_id_abstain.json",
            ),
        }

        # when
        sync_docs: dict[str, str] = {
            name: inspect.getdoc(getattr(NexusV1Client, name)) or "" for name in suffixes
        }
        async_docs: dict[str, str] = {
            name: inspect.getdoc(getattr(AsyncNexusV1Client, name)) or ""
            for name in suffixes
        }

        # then
        assert all(
            all(f"{base_url}{suffix}" in sync_docs[name] for suffix in expected)
            for name, expected in suffixes.items()
        )
        assert sync_docs == async_docs
        assert base_url not in (inspect.getdoc(NexusV1Client.get_file_content) or "")

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
        endorsement = client.get_endorsements()[0]
        assert endorsement.status == "Endorsed"
        assert endorsement.date.year == 2026
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

    def test_returns_empty_md5_results_for_not_found_response(self) -> None:
        """Tests that an unmatched MD5 search produces an empty result list."""

        # given
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(404, json={"message": "Not found"})

        client = NexusV1Client(
            NexusConfig(v1_base_url="http://127.0.0.1/v1"),
            http_client=httpx.Client(transport=httpx.MockTransport(handler)),
        )

        # when
        results = client.search_file_by_md5("game", "0" * 32)

        # then
        assert results == []
        client.close()

    def test_accepts_legacy_numeric_endorsement_date(self) -> None:
        """Tests compatibility with the former Unix timestamp response shape."""

        # given / when
        endorsement = Endorsement.model_validate(
            {
                "mod_id": 2,
                "domain_name": "game",
                "date": 1,
                "status": "Endorsed",
            }
        )

        # then
        assert endorsement.date == datetime.fromtimestamp(1, UTC)

    def test_closes_owned_client_context(self) -> None:
        """Tests synchronous context-managed ownership."""

        # given
        client: NexusV1Client = NexusV1Client()

        # when
        with client:
            pass

        # then
        assert True
