"""Copyright (c) Modding Forge."""

import pytest
from pydantic import ValidationError

from nexusmods_api.nexus_config import NexusConfig


class TestNexusConfig:
    """Tests `nexusmods_api.nexus_config.NexusConfig`."""

    def test_normalizes_service_urls(self) -> None:
        """Tests that trailing slashes are removed from service URLs."""

        # given / when
        config: NexusConfig = NexusConfig(v1_base_url="https://example.com/v1/")

        # then
        assert config.v1_base_url == "https://example.com/v1"

    def test_accepts_local_http_test_server(self) -> None:
        """Tests that local test servers may use an unencrypted connection."""

        # given / when
        config: NexusConfig = NexusConfig(v2_url="http://127.0.0.1:8000/graphql")

        # then
        assert config.v2_url.startswith("http://127.0.0.1")

    def test_rejects_insecure_remote_url(self) -> None:
        """Tests that remote service overrides must use HTTPS."""

        # given / when / then
        with pytest.raises(ValidationError):
            NexusConfig(v3_base_url="http://example.com/v3")

    def test_normalizes_secure_websocket_url(self) -> None:
        """Tests that a secure WebSocket URL is normalized."""

        # given / when
        config: NexusConfig = NexusConfig(sso_url="wss://example.com/")

        # then
        assert config.sso_url == "wss://example.com"

    def test_rejects_insecure_remote_websocket_url(self) -> None:
        """Tests that remote WebSocket overrides must use WSS."""

        # given / when / then
        with pytest.raises(ValidationError):
            NexusConfig(sso_url="ws://example.com")
