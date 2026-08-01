"""Copyright (c) Modding Forge."""

from typing import cast

import httpx
from pydantic import TypeAdapter, ValidationError

from ..errors.factory import sanitize_url
from ..errors.nexus_response_validation_error import NexusResponseValidationError
from ..types import JsonValue


def parse_response[ResponseT](
    response: httpx.Response,
    response_model: type[ResponseT],
) -> ResponseT:
    """Validates a successful JSON response against a target type.

    Args:
        response (httpx.Response): Successful HTTP response.
        response_model (type[ResponseT]): Pydantic-compatible target type.

    Returns:
        ResponseT: Validated response value.

    Raises:
        NexusResponseValidationError: If JSON decoding or validation fails.
    """

    try:
        payload: object = cast(object, response.json())
        return TypeAdapter(response_model).validate_python(payload)
    except (ValueError, ValidationError) as error:
        raise NexusResponseValidationError(
            "Nexus Mods returned an invalid response payload.",
            status_code=response.status_code,
            request_url=sanitize_url(response.request.url),
        ) from error


def parse_json_response(response: httpx.Response) -> JsonValue:
    """Validates a successful response as a recursive JSON value.

    Args:
        response (httpx.Response): Successful HTTP response.

    Returns:
        JsonValue: Validated response data.

    Raises:
        NexusResponseValidationError: If JSON decoding or validation fails.
    """

    try:
        payload: object = cast(object, response.json())
        adapter: TypeAdapter[JsonValue] = TypeAdapter(JsonValue)
        return adapter.validate_python(payload)
    except (ValueError, ValidationError) as error:
        raise NexusResponseValidationError(
            "Nexus Mods returned an invalid response payload.",
            status_code=response.status_code,
            request_url=sanitize_url(response.request.url),
        ) from error
