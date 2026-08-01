"""Executable WebSocket SSO construction example."""

from nexusmods_api.sso import SSOConfig, SSOFlow


def sso_flow(application_id: str) -> SSOFlow:
    """Builds a synchronous SSO flow without connecting."""

    return SSOFlow(SSOConfig(application_id=application_id))
