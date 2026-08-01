"""Executable quickstart example."""

from nexusmods_api import ApiKeyAuth, NexusClient, NexusConfig


def build_client(api_key: str) -> NexusClient:
    """Builds a lazy client without sending a request."""

    config = NexusConfig(
        application_name="your-registered-app",
        application_version="1.0.0",
    )
    return NexusClient(config, ApiKeyAuth.from_value(api_key))
