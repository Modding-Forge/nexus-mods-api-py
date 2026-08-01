"""Copyright (c) Modding Forge."""

import httpx
import pytest
from pydantic import BaseModel, ConfigDict

from nexusmods_api.errors.nexus_response_validation_error import (
    NexusResponseValidationError,
)
from nexusmods_api.transport.response import parse_json_response, parse_response
from nexusmods_api.types import JsonValue


class TestResponseParsing:
    """Tests validated successful response parsing."""

    class Payload(BaseModel):
        """Represents a small response parsing fixture."""

        model_config = ConfigDict(frozen=True, use_attribute_docstrings=True)

        value: int
        """The fixture value."""

    def test_parses_response_model(self) -> None:
        """Tests that JSON data validates against a supplied model."""

        # given
        response: httpx.Response = httpx.Response(
            200,
            json={"value": 3},
            request=httpx.Request("GET", "https://example.com"),
        )

        # when
        result: TestResponseParsing.Payload = parse_response(response, self.Payload)

        # then
        assert result.value == 3

    def test_parses_recursive_json(self) -> None:
        """Tests that arbitrary JSON responses retain nested values."""

        # given
        response: httpx.Response = httpx.Response(
            200,
            json={"items": [1, None]},
            request=httpx.Request("GET", "https://example.com"),
        )

        # when
        result: JsonValue = parse_json_response(response)

        # then
        assert result == {"items": [1, None]}

    def test_wraps_model_validation_failure(self) -> None:
        """Tests that invalid upstream data raises a sanitized client error."""

        # given
        response: httpx.Response = httpx.Response(
            200,
            json={"value": "invalid"},
            request=httpx.Request("GET", "https://example.com?token=secret"),
        )

        # when / then
        with pytest.raises(NexusResponseValidationError) as error_info:
            parse_response(response, self.Payload)
        assert error_info.value.request_url == "https://example.com"

    def test_wraps_invalid_json(self) -> None:
        """Tests that a malformed JSON body raises a response validation error."""

        # given
        response: httpx.Response = httpx.Response(
            200,
            content=b"not-json",
            request=httpx.Request("GET", "https://example.com"),
        )

        # when / then
        with pytest.raises(NexusResponseValidationError):
            parse_json_response(response)
