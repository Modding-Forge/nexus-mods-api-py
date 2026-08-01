"""Executable sync and async construction example."""

from nexusmods_api import ApiKeyAuth, AsyncNexusClient, NexusClient


def sync_client(api_key: str) -> NexusClient:
    """Builds the synchronous aggregate."""

    return NexusClient(auth=ApiKeyAuth.from_value(api_key))


def async_client(api_key: str) -> AsyncNexusClient:
    """Builds the asynchronous aggregate."""

    return AsyncNexusClient(auth=ApiKeyAuth.from_value(api_key))
