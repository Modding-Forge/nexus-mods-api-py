"""Copyright (c) Modding Forge."""

from .nexus_authentication_error import NexusAuthenticationError


class NexusOAuthError(NexusAuthenticationError):
    """Reports a sanitized OAuth authorization or token failure."""
