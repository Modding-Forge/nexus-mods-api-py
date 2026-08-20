"""Copyright (c) Modding Forge."""

import asyncio
from pathlib import Path

import httpx
import pytest

from nexusmods_api import FileContent
from nexusmods_api.auth.api_key_auth import ApiKeyAuth
from nexusmods_api.errors.nexus_http_error import NexusHttpError
from nexusmods_api.errors.nexus_response_validation_error import (
    NexusResponseValidationError,
)
from nexusmods_api.errors.nexus_transport_error import NexusTransportError
from nexusmods_api.nexus_config import NexusConfig
from nexusmods_api.v1.async_nexus_v1_client import AsyncNexusV1Client
from nexusmods_api.v1.nexus_v1_client import NexusV1Client
from nexusmods_api.v1.validators import require_content_preview_url


class TestFileContentClients:
    """Tests synchronous and asynchronous file-content convenience methods."""

    PREVIEW_URL: str = "https://preview.example/archive?signature=private"

    def test_sync_fetches_preview_without_credentials_and_retries(self) -> None:
        """Flattens a retried response without forwarding configured secrets."""

        # given
        requests: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            """Returns one transient failure followed by a preview tree.

            Returns:
                httpx.Response: Transient or successful preview response.
            """

            requests.append(request)
            if len(requests) == 1:
                return httpx.Response(503, headers={"Retry-After": "0"})
            return httpx.Response(
                200,
                json={
                    "children": [
                        {"type": "file", "path": "Data/Example.esm"},
                    ]
                },
            )

        http_client: httpx.Client = httpx.Client(
            headers={"Authorization": "Bearer secret", "apikey": "default-key"},
            transport=httpx.MockTransport(handler),
        )
        client: NexusV1Client = NexusV1Client(
            auth=ApiKeyAuth.from_value("configured-key"),
            http_client=http_client,
        )

        # when
        result: FileContent = client.get_file_content(self.PREVIEW_URL)

        # then
        assert result.paths == [Path("Data/Example.esm")]
        assert len(requests) == 2
        assert all("Authorization" not in request.headers for request in requests)
        assert all("apikey" not in request.headers for request in requests)
        client.close()
        http_client.close()

    async def test_async_fetches_equivalent_preview_without_credentials(self) -> None:
        """Provides native async parity without forwarding configured secrets."""

        # given
        requests: list[httpx.Request] = []

        async def handler(request: httpx.Request) -> httpx.Response:
            """Returns one valid asynchronous preview response.

            Returns:
                httpx.Response: Successful preview response.
            """

            requests.append(request)
            return httpx.Response(
                200,
                json={
                    "children": [
                        {"type": "file", "path": "Data/Example.esm"},
                    ]
                },
            )

        http_client: httpx.AsyncClient = httpx.AsyncClient(
            headers={"Authorization": "Bearer secret", "apikey": "default-key"},
            transport=httpx.MockTransport(handler),
        )
        client: AsyncNexusV1Client = AsyncNexusV1Client(
            auth=ApiKeyAuth.from_value("configured-key"),
            http_client=http_client,
        )

        # when
        result: FileContent = await client.get_file_content(self.PREVIEW_URL)

        # then
        assert result.paths == [Path("Data/Example.esm")]
        assert "Authorization" not in requests[0].headers
        assert "apikey" not in requests[0].headers
        await client.close()
        await http_client.aclose()

    @pytest.mark.parametrize(
        "value",
        [
            None,
            "",
            " ",
            "relative/path",
            "ftp://preview.example/archive",
            "http://preview.example/archive",
            "https://user:password@preview.example/archive",
            "https://preview.example/archive#fragment",
            " https://preview.example/archive",
        ],
    )
    def test_rejects_missing_or_unsafe_preview_urls(self, value: str | None) -> None:
        """Rejects ambiguous URLs before any external network operation."""

        # given / when / then
        with pytest.raises(ValueError, match=r"content.preview|Non-local"):
            require_content_preview_url(value)

    @pytest.mark.parametrize(
        "value",
        [
            "https://preview.example/archive?signature=value",
            "http://127.0.0.1:8080/archive",
            "http://localhost/archive",
            "http://[::1]/archive",
        ],
    )
    def test_accepts_secure_and_loopback_preview_urls(self, value: str) -> None:
        """Preserves valid signed and local test URLs without normalization."""

        # given / when
        result: str = require_content_preview_url(value)

        # then
        assert result == value

    def test_maps_http_json_shape_and_network_failures(self) -> None:
        """Uses the established safe exception hierarchy for preview failures."""

        # given
        responses: list[httpx.Response | Exception] = [
            httpx.Response(404, json={"message": "missing"}),
            httpx.Response(200, content=b"invalid-json"),
            httpx.Response(200, json={"type": "file", "path": "../secret"}),
            httpx.ConnectError("internal network detail"),
        ]

        def handler(request: httpx.Request) -> httpx.Response:
            """Returns or raises each configured failure in sequence.

            Returns:
                httpx.Response: Configured HTTP response.

            Raises:
                httpx.ConnectError: For the configured network failure.
            """

            outcome: httpx.Response | Exception = responses.pop(0)
            if isinstance(outcome, Exception):
                raise httpx.ConnectError(str(outcome), request=request)
            return outcome

        client: NexusV1Client = NexusV1Client(
            NexusConfig(max_retries=0),
            http_client=httpx.Client(transport=httpx.MockTransport(handler)),
        )

        # when / then
        with pytest.raises(NexusHttpError) as http_error:
            client.get_file_content(self.PREVIEW_URL)
        with pytest.raises(NexusResponseValidationError):
            client.get_file_content(self.PREVIEW_URL)
        with pytest.raises(NexusResponseValidationError):
            client.get_file_content(self.PREVIEW_URL)
        with pytest.raises(NexusTransportError) as transport_error:
            client.get_file_content(self.PREVIEW_URL)
        assert http_error.value.request_url == "https://preview.example/archive"
        assert transport_error.value.request_url == "https://preview.example/archive"
        assert "private" not in repr(http_error.value)
        assert "network detail" not in repr(transport_error.value)
        client.close()

    async def test_async_preserves_network_failure_and_cancellation(self) -> None:
        """Preserves async transport errors and task cancellation semantics."""

        # given
        attempts: list[int] = []

        async def handler(request: httpx.Request) -> httpx.Response:
            """Raises a network failure and then task cancellation.

            Raises:
                httpx.ConnectError: On the first operation.
                asyncio.CancelledError: On the second operation.
            """

            attempts.append(len(attempts))
            if len(attempts) == 1:
                raise httpx.ConnectError("internal detail", request=request)
            raise asyncio.CancelledError

        client: AsyncNexusV1Client = AsyncNexusV1Client(
            NexusConfig(max_retries=0),
            http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
        )

        # when / then
        with pytest.raises(NexusTransportError):
            await client.get_file_content(self.PREVIEW_URL)
        with pytest.raises(asyncio.CancelledError):
            await client.get_file_content(self.PREVIEW_URL)
        await client.close()
