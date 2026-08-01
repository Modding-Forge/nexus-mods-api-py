"""Executable REST v1 construction example."""

from nexusmods_api import ApiKeyAuth, NexusV1Client


def client(api_key: str) -> NexusV1Client:
    """Builds a focused synchronous REST v1 client."""

    return NexusV1Client(auth=ApiKeyAuth.from_value(api_key))
