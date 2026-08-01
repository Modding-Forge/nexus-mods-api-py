"""Copyright (c) Modding Forge."""

import base64
import hashlib
import secrets
from urllib.parse import urlencode

from pydantic import SecretStr

from .oauth_authorization import OAuthAuthorization
from .oauth_client_config import OAuthClientConfig


def create_pkce_authorization(
    client_config: OAuthClientConfig,
    oauth_base_url: str,
) -> OAuthAuthorization:
    """Creates a fresh RFC 7636 S256 authorization attempt.

    Args:
        client_config (OAuthClientConfig): Registered caller application.
        oauth_base_url (str): Nexus Mods OAuth service base URL.

    Returns:
        OAuthAuthorization: Headless authorization instructions.
    """

    verifier: str = secrets.token_urlsafe(64)
    state: str = secrets.token_urlsafe(32)
    digest: bytes = hashlib.sha256(verifier.encode("ascii")).digest()
    challenge: str = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
    query: str = urlencode(
        {
            "client_id": client_config.client_id,
            "response_type": "code",
            "scope": " ".join(client_config.scopes),
            "redirect_uri": client_config.redirect_uri,
            "state": state,
            "code_challenge_method": "S256",
            "code_challenge": challenge,
        }
    )
    return OAuthAuthorization(
        authorization_url=f"{oauth_base_url}/authorize?{query}",
        state=SecretStr(state),
        code_verifier=SecretStr(verifier),
    )
