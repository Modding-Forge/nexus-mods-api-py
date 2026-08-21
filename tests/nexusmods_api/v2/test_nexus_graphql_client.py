"""Copyright (c) Modding Forge."""

import inspect
import json
from typing import cast

import httpx
import pytest

from nexusmods_api.errors.nexus_graphql_error import NexusGraphQLError
from nexusmods_api.errors.nexus_response_validation_error import (
    NexusResponseValidationError,
)
from nexusmods_api.nexus_config import NexusConfig
from nexusmods_api.types import JsonValue
from nexusmods_api.v2.async_nexus_graphql_client import AsyncNexusGraphQLClient
from nexusmods_api.v2.nexus_graphql_client import NexusGraphQLClient

from .payloads import operation_payload


class TestNexusGraphQLClient:
    """Tests the generic and convenient synchronous GraphQL v2 surface."""

    def test_endpoint_docstrings_link_official_queries(self) -> None:
        """Tests official GraphQL links and sync/async documentation parity."""

        # given
        links: dict[str, str] = {
            "execute": "https://graphql.nexusmods.com/#introduction",
            "execute_raw": "https://graphql.nexusmods.com/#introduction",
            "get_games": "https://graphql.nexusmods.com/#query-games",
            "get_mod": "https://graphql.nexusmods.com/#query-mod",
            "search_mods": "https://graphql.nexusmods.com/#query-mods",
            "get_mod_files": "https://graphql.nexusmods.com/#query-modFiles",
            "get_collection": "https://graphql.nexusmods.com/#query-collection",
            "get_revision": ("https://graphql.nexusmods.com/#query-collectionRevision"),
            "get_user": "https://graphql.nexusmods.com/#query-user",
        }

        # when
        sync_docs: dict[str, str] = {
            name: inspect.getdoc(getattr(NexusGraphQLClient, name)) or ""
            for name in links
        }
        async_docs: dict[str, str] = {
            name: inspect.getdoc(getattr(AsyncNexusGraphQLClient, name)) or ""
            for name in links
        }

        # then
        assert all(link in sync_docs[name] for name, link in links.items())
        assert sync_docs == async_docs

    def test_executes_all_convenience_queries(self) -> None:
        """Tests typed convenience roots, variables, and pagination."""

        # given
        requests: list[dict[str, JsonValue]] = []

        def handler(request: httpx.Request) -> httpx.Response:
            payload: dict[str, JsonValue] = cast(
                dict[str, JsonValue],
                json.loads(request.content),
            )
            requests.append(payload)
            operation_name: JsonValue = payload.get("operationName")
            return httpx.Response(
                200,
                json=operation_payload(
                    operation_name if isinstance(operation_name, str) else None
                ),
            )

        http_client: httpx.Client = httpx.Client(transport=httpx.MockTransport(handler))
        client: NexusGraphQLClient = NexusGraphQLClient(
            NexusConfig(v2_url="http://127.0.0.1/graphql"),
            http_client=http_client,
        )

        # when / then
        assert client.get_games(count=1).nodes[0].domain_name == "game"
        assert client.get_mod("4294967298").mod_id == 2
        assert client.search_mods("Mod").nodes[0].name == "Mod"
        assert client.get_mod_files("4294967298").nodes[0].file_id == 4
        assert client.get_collection("collection").id == 3
        assert client.get_revision("collection", 1).id == 5
        assert client.get_user(6).member_id == 6
        assert requests[0]["operationName"] == "Games"
        assert requests[1]["variables"] == {"modId": "2", "gameId": "1"}
        assert requests[2]["variables"] == {
            "filter": {
                "name": [{"value": "Mod", "op": "WILDCARD"}],
            },
            "count": 20,
            "offset": 0,
        }
        assert client.last_errors == ()
        assert client.rate_limits.daily_remaining is None
        client.close()
        assert http_client.is_closed is False
        http_client.close()

    def test_handles_errors_partial_data_and_raw_envelopes(self) -> None:
        """Tests strict errors, partial opt-in, and raw envelope preservation."""

        # given
        responses: list[dict[str, JsonValue]] = [
            {
                "data": {"answer": 42},
                "errors": [
                    {
                        "message": "field failed",
                        "locations": [{"line": 1, "column": 2}],
                        "path": ["answer"],
                    }
                ],
            },
            {
                "data": {"answer": 42},
                "errors": [{"message": "field failed"}],
            },
            {
                "data": {"answer": 42},
                "errors": [{"message": "field failed"}],
            },
        ]

        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json=responses.pop(0))

        client: NexusGraphQLClient = NexusGraphQLClient(
            NexusConfig(v2_url="http://127.0.0.1/graphql"),
            http_client=httpx.Client(transport=httpx.MockTransport(handler)),
        )

        # when / then
        with pytest.raises(NexusGraphQLError, match="1 error"):
            client.execute("query { answer }", dict[str, int])
        partial: dict[str, int] = client.execute(
            "query { answer }",
            dict[str, int],
            allow_partial=True,
        )
        assert partial == {"answer": 42}
        assert client.last_errors[0].locations is None
        raw = client.execute_raw("query { answer }")
        assert raw.data == {"answer": 42}
        assert len(client.last_errors) == 1
        client.close()

    @pytest.mark.parametrize(
        "envelope",
        [
            {},
            {"data": {"answer": "not-an-int"}},
        ],
    )
    def test_rejects_missing_or_invalid_data(
        self,
        envelope: dict[str, JsonValue],
    ) -> None:
        """Tests safe validation failures for malformed GraphQL data."""

        # given
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json=envelope)

        client: NexusGraphQLClient = NexusGraphQLClient(
            NexusConfig(v2_url="http://127.0.0.1/graphql"),
            http_client=httpx.Client(transport=httpx.MockTransport(handler)),
        )

        # when / then
        with pytest.raises(NexusResponseValidationError):
            client.execute(
                "query { answer }",
                dict[str, int],
                allow_partial=True,
            )
        client.close()

    def test_rejects_missing_convenience_root_and_closes_context(self) -> None:
        """Tests required root validation and context cleanup."""

        # given
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json={"data": {"other": {"uid": "x"}}})

        client: NexusGraphQLClient = NexusGraphQLClient(
            NexusConfig(v2_url="http://127.0.0.1/graphql"),
            http_client=httpx.Client(transport=httpx.MockTransport(handler)),
        )

        # when / then
        with pytest.raises(NexusResponseValidationError, match="mod field"):
            client.get_mod("4294967298")
        client.close()
        with NexusGraphQLClient():
            pass

    @pytest.mark.parametrize("uid", ["invalid", "-1", str(1 << 64)])
    def test_rejects_invalid_mod_uid(self, uid: str) -> None:
        """Tests that convenience mod reads reject malformed UIDs."""

        # given
        client = NexusGraphQLClient()

        # when / then
        with pytest.raises(ValueError, match="mod UID"):
            client.get_mod(uid)
        with pytest.raises(ValueError, match="mod UID"):
            client.get_mod_files(uid)
        client.close()
