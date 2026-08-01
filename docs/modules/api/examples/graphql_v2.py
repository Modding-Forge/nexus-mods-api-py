"""Executable GraphQL v2 construction example."""

from nexusmods_api import ApiKeyAuth, NexusGraphQLClient


def client(api_key: str) -> NexusGraphQLClient:
    """Builds a focused synchronous GraphQL v2 client."""

    return NexusGraphQLClient(auth=ApiKeyAuth.from_value(api_key))
