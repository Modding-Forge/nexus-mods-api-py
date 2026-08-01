"""Copyright (c) Modding Forge."""

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
from nexusmods_api.v2.nexus_graphql_client import NexusGraphQLClient

from .payloads import operation_payload


class TestNexusGraphQLClient:
    """Tests the generic and convenient synchronous GraphQL v2 surface."""

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

        http_client: httpx.Client = httpx.Client(
            transport=httpx.MockTransport(handler)
        )
        client: NexusGraphQLClient = NexusGraphQLClient(
            NexusConfig(v2_url="http://127.0.0.1/graphql"),
            http_client=http_client,
        )

        # when / then
        assert client.get_games(count=1).nodes[0].domain_name == "game"
        assert client.get_mod("game:2").mod_id == 2
        assert client.search_mods("Mod").nodes[0].name == "Mod"
        assert client.get_mod_files("game:2").nodes[0].file_id == 4
        assert client.get_collection("collection").id == 3
        assert client.get_revision(5).revision_number == 1
        assert client.get_user(6).member_id == 6
        assert requests[0]["operationName"] == "Games"
        assert requests[1]["variables"] == {"uid": "game:2"}
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
            client.get_mod("x")
        client.close()
        with NexusGraphQLClient():
            pass
