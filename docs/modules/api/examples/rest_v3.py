"""Executable REST v3 construction example."""

from nexusmods_api import ApiKeyAuth, NexusV3Client


def client(api_key: str) -> NexusV3Client:
    """Builds a focused synchronous REST v3 client."""

    return NexusV3Client(auth=ApiKeyAuth.from_value(api_key))
