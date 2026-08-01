"""Executable headless OAuth PKCE example."""

from nexusmods_api import NexusConfig, OAuthClientConfig, OAuthFlow


def authorization_url(client_id: str, redirect_uri: str) -> str:
    """Creates a fresh headless authorization URL."""

    flow = OAuthFlow(
        OAuthClientConfig(client_id=client_id, redirect_uri=redirect_uri),
        NexusConfig(),
    )
    try:
        return flow.create_authorization().authorization_url
    finally:
        flow.close()
