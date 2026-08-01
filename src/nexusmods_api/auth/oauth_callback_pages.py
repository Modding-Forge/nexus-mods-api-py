"""Copyright (c) Modding Forge."""

from pydantic import ConfigDict, Field

from ..models.request_model import RequestModel

DEFAULT_SUCCESS_HTML: str = (
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    "<title>Authorization received</title></head><body><main>"
    "<h1>Authorization received</h1>"
    "<p>You may close this window.</p></main></body></html>"
)
"""Default browser page shown after a captured OAuth callback."""

DEFAULT_ERROR_HTML: str = (
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    "<title>Authorization failed</title></head><body><main>"
    "<h1>Authorization failed</h1>"
    "<p>The callback request could not be accepted.</p></main></body></html>"
)
"""Default browser page shown for an invalid OAuth callback request."""


class OAuthCallbackPages(RequestModel):
    """Defines static HTML returned by OAuth loopback callback servers."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        use_attribute_docstrings=True,
    )

    success_html: str = Field(default=DEFAULT_SUCCESS_HTML, min_length=1)
    """Static HTML returned after a matching callback is captured."""

    error_html: str = Field(default=DEFAULT_ERROR_HTML, min_length=1)
    """Static HTML returned for a malformed or unrelated callback request."""
