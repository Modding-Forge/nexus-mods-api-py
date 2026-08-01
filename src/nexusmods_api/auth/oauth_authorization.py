"""Copyright (c) Modding Forge."""

from pydantic import ConfigDict, Field, SecretStr

from ..models.request_model import RequestModel


class OAuthAuthorization(RequestModel):
    """Carries one short-lived PKCE authorization attempt."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        use_attribute_docstrings=True,
    )

    authorization_url: str = Field(repr=False)
    """The Nexus Mods URL that the user must open."""

    state: SecretStr = Field(repr=False)
    """The secret anti-forgery value expected on the callback."""

    code_verifier: SecretStr = Field(repr=False)
    """The secret PKCE verifier retained for the token exchange."""
