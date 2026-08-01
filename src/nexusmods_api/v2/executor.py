"""Copyright (c) Modding Forge."""

import httpx
from pydantic import TypeAdapter, ValidationError

from ..errors.factory import sanitize_url
from ..errors.nexus_graphql_error import NexusGraphQLError
from ..errors.nexus_response_validation_error import NexusResponseValidationError
from ..transport.response import parse_response
from .models.graphql_issue import GraphQLIssue
from .models.graphql_response import GraphQLResponse


def parse_graphql_data[ResponseT](
    response: httpx.Response,
    response_model: type[ResponseT],
    *,
    allow_partial: bool,
) -> tuple[ResponseT, tuple[GraphQLIssue, ...]]:
    """Validates a GraphQL envelope and its typed data member.

    Args:
        response (httpx.Response): Successful HTTP response.
        response_model (type[ResponseT]): Expected GraphQL data type.
        allow_partial (bool): Whether data accompanied by errors is accepted.

    Returns:
        tuple[ResponseT, tuple[GraphQLIssue, ...]]: Typed data and reported issues.

    Raises:
        NexusGraphQLError: If GraphQL reports disallowed execution errors.
        NexusResponseValidationError: If the data member is absent or malformed.
    """

    envelope: GraphQLResponse = parse_response(response, GraphQLResponse)
    issues: tuple[GraphQLIssue, ...] = tuple(envelope.errors or ())
    if issues and not allow_partial:
        raise NexusGraphQLError(
            f"The GraphQL operation returned {len(issues)} error(s).",
            status_code=response.status_code,
            request_url=sanitize_url(response.request.url),
        )
    if envelope.data is None:
        raise NexusResponseValidationError(
            "The GraphQL response did not contain data.",
            status_code=response.status_code,
            request_url=sanitize_url(response.request.url),
        )
    try:
        data: ResponseT = TypeAdapter(response_model).validate_python(envelope.data)
    except ValidationError as error:
        raise NexusResponseValidationError(
            "Nexus Mods returned invalid GraphQL data.",
            status_code=response.status_code,
            request_url=sanitize_url(response.request.url),
        ) from error
    return data, issues
