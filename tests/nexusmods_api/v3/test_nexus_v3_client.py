"""Copyright (c) Modding Forge."""

import hashlib
import inspect
import re
import warnings
from collections.abc import Callable
from pathlib import Path
from typing import Optional, cast

import httpx
import pytest

from nexusmods_api.nexus_config import NexusConfig
from nexusmods_api.types import JsonValue
from nexusmods_api.v3.generated import models as generated_models
from nexusmods_api.v3.generated.operations import OPERATIONS
from nexusmods_api.v3.nexus_stability_warning import NexusStabilityWarning
from nexusmods_api.v3.nexus_v3_client import NexusV3Client


class TestNexusV3Client:
    """Tests generated synchronous REST v3 coverage and validation."""

    EXPECTED_HASH: str = (
        "15a82a80cc3e0ec1a47f7ae50ca6a0236eb6fccf84a298b06eb02b6db978e644"
    )

    def test_snapshot_registry_and_models_are_complete(self) -> None:
        """Tests pinned provenance and generated operation/model counts."""

        # given
        root: Path = Path(__file__).resolve().parents[3]
        snapshot: Path = root / "specs" / "nexusmods-v3-openapi.yaml"

        # when
        digest: str = hashlib.sha256(snapshot.read_bytes()).hexdigest()

        # then
        assert digest == self.EXPECTED_HASH
        assert len(OPERATIONS) == 33
        assert len(generated_models.__all__) == 84
        model_class = getattr(generated_models, generated_models.__all__[0])
        assert model_class.model_config["extra"] == "allow"

    def test_generated_api_has_complete_source_documentation(self) -> None:
        """Tests generated model fields and operation methods are documented."""

        # given
        operation_names: list[str] = [
            self.__method_name(operation.operation_id)
            for operation in OPERATIONS.values()
        ]

        # when
        model_descriptions: list[Optional[str]] = [
            field.description
            for model_name in generated_models.__all__
            for field in getattr(generated_models, model_name).model_fields.values()
        ]
        operation_docstrings: list[str] = [
            inspect.getdoc(getattr(NexusV3Client, operation_name)) or ""
            for operation_name in operation_names
        ]

        # then
        assert model_descriptions
        assert all(model_descriptions)
        assert all("Args:" in docstring for docstring in operation_docstrings)
        assert all("Returns:" in docstring for docstring in operation_docstrings)
        assert all(
            "Original API documentation: https://api-docs.nexusmods.com/#tag/"
            in docstring
            for docstring in operation_docstrings
        )
        assert (
            "https://api-docs.nexusmods.com/#tag/mods/operation/getMod"
            in (inspect.getdoc(NexusV3Client.get_mod) or "")
        )

    def test_invokes_every_generated_operation(self) -> None:
        """Tests every explicit generated method against its registry metadata."""

        # given
        requests: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            return httpx.Response(200, json={"ok": True})

        http_client: httpx.Client = httpx.Client(transport=httpx.MockTransport(handler))
        client: NexusV3Client = NexusV3Client(
            NexusConfig(
                v3_base_url="http://127.0.0.1/v3",
                warn_on_unstable=False,
            ),
            http_client=http_client,
        )

        # when
        for operation in OPERATIONS.values():
            method = cast(
                Callable[..., JsonValue],
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
            assert method(**arguments) == {"ok": True}

        # then
        assert len(requests) == len(OPERATIONS)
        assert len(client.operations) == len(OPERATIONS)
        assert client.rate_limits.daily_remaining is None
        client.close()
        assert http_client.is_closed is False
        http_client.close()

    def test_typed_request_no_content_and_parameter_errors(self) -> None:
        """Tests typed generic requests, 204 responses, and local validation."""

        # given
        statuses: list[int] = [200, 204]

        def handler(request: httpx.Request) -> httpx.Response:
            status: int = statuses.pop(0)
            return httpx.Response(
                status,
                json={"ok": True} if status == 200 else None,
            )

        client: NexusV3Client = NexusV3Client(
            NexusConfig(
                v3_base_url="http://127.0.0.1/v3",
                warn_on_unstable=False,
            ),
            http_client=httpx.Client(transport=httpx.MockTransport(handler)),
        )

        # when / then
        assert client.request(
            "getTrendingMods",
            dict[str, bool],
            path_parameters={"game_domain": "game/name"},
        ) == {"ok": True}
        assert client.edit_collection(1, body={"name": "New"}) is None
        with pytest.raises(ValueError, match="Unknown"):
            client.request_json("unknown")
        with pytest.raises(ValueError, match="missing"):
            client.request_json("getMod", path_parameters={"game_domain": "game"})
        client.close()

    def test_warns_once_for_experimental_operation(self) -> None:
        """Tests the process-wide filterable stability warning."""

        # given
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json=[])

        client: NexusV3Client = NexusV3Client(
            NexusConfig(v3_base_url="http://127.0.0.1/v3"),
            http_client=httpx.Client(transport=httpx.MockTransport(handler)),
        )

        # when
        with warnings.catch_warnings(record=True) as captured:
            warnings.simplefilter("always", NexusStabilityWarning)
            client.get_game_dlcs("game")
            client.get_game_dlcs("game")

        # then
        stability_warnings = [
            item for item in captured if issubclass(item.category, NexusStabilityWarning)
        ]
        assert len(stability_warnings) == 1
        assert "getGameDlcs" in str(stability_warnings[0].message)
        client.close()

    def test_closes_owned_context(self) -> None:
        """Tests synchronous context-managed cleanup."""

        # given / when / then
        with NexusV3Client():
            pass

    @staticmethod
    def __method_name(operation_id: str) -> str:
        """Converts an operation ID to its generated method name.

        Args:
            operation_id (str): OpenAPI operation identifier.

        Returns:
            str: Generated snake-case method name.
        """

        return re.sub(r"(?<!^)(?=[A-Z])", "_", operation_id).lower()
