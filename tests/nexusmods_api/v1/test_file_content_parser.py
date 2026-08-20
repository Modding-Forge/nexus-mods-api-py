"""Copyright (c) Modding Forge."""

from pathlib import Path
from typing import cast

import httpx
import pytest

from nexusmods_api.errors.nexus_response_validation_error import (
    NexusResponseValidationError,
)
from nexusmods_api.types import JsonValue
from nexusmods_api.v1.file_content_parser import parse_file_content
from nexusmods_api.v1.models.file_content import FileContent


class TestFileContentParser:
    """Tests content-preview tree validation and flattening."""

    def test_flattens_nested_files_in_order_with_duplicates(self) -> None:
        """Preserves traversal order, spelling, and duplicate file entries."""

        # given
        payload: JsonValue = {
            "type": "directory",
            "name": "root",
            "children": [
                {
                    "type": "directory",
                    "name": "Data",
                    "future_field": True,
                    "children": [
                        {"type": "file", "path": "Data/Plugin.esp"},
                        {"type": "file", "path": "Data/Plugin.esp"},
                    ],
                },
                {"type": "file", "path": "README.txt", "checksum": "future"},
            ],
        }
        response: httpx.Response = self._response(payload)

        # when
        result: FileContent = parse_file_content(response)

        # then
        assert result.paths == [
            Path("Data/Plugin.esp"),
            Path("Data/Plugin.esp"),
            Path("README.txt"),
        ]

    @pytest.mark.parametrize(
        "payload",
        [
            {"type": "directory", "children": []},
            {"children": []},
            {"type": "directory"},
        ],
    )
    def test_accepts_empty_archives_and_directories(self, payload: JsonValue) -> None:
        """Returns an empty path list for valid trees without file nodes."""

        # given
        response: httpx.Response = self._response(payload)

        # when
        result: FileContent = parse_file_content(response)

        # then
        assert result.paths == []

    @pytest.mark.parametrize(
        "payload",
        [
            cast(JsonValue, []),
            cast(JsonValue, {"name": "root"}),
            cast(JsonValue, {"type": "file"}),
            cast(JsonValue, {"type": "file", "path": ""}),
            cast(JsonValue, {"type": "file", "path": "../secret.txt"}),
            cast(JsonValue, {"type": "file", "path": "/absolute.txt"}),
            cast(JsonValue, {"type": "file", "path": "C:\\absolute.txt"}),
            cast(
                JsonValue,
                {"type": "file", "path": "file.txt", "children": []},
            ),
        ],
    )
    def test_rejects_malformed_trees_and_paths(self, payload: JsonValue) -> None:
        """Maps invalid shapes and unsafe paths to the response error hierarchy."""

        # given
        response: httpx.Response = self._response(payload)

        # when
        with pytest.raises(NexusResponseValidationError) as captured:
            parse_file_content(response)

        # then
        assert captured.value.request_url == "https://preview.example/archive"
        assert "secret" not in str(captured.value)

    def test_rejects_invalid_json(self) -> None:
        """Maps JSON decoding failures to a sanitized validation error."""

        # given
        request: httpx.Request = httpx.Request(
            "GET",
            "https://preview.example/archive?token=secret",
        )
        response: httpx.Response = httpx.Response(
            200,
            request=request,
            content=b"not-json",
        )

        # when
        with pytest.raises(NexusResponseValidationError) as captured:
            parse_file_content(response)

        # then
        assert captured.value.request_url == "https://preview.example/archive"
        assert "secret" not in str(captured.value)

    @staticmethod
    def _response(payload: JsonValue) -> httpx.Response:
        """Builds a successful response containing a JSON payload.

        Args:
            payload (JsonValue): Preview payload to encode.

        Returns:
            httpx.Response: Test response with a bound request.
        """

        request: httpx.Request = httpx.Request(
            "GET",
            "https://preview.example/archive?token=secret",
        )
        return httpx.Response(200, request=request, json=payload)
