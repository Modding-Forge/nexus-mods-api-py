"""Copyright (c) Modding Forge."""

import json
from unittest.mock import MagicMock
from uuid import UUID

import pytest
from pytest_mock import MockerFixture

from nexusmods_api.auth.sso_config import SSOConfig
from nexusmods_api.auth.sso_flow import SSOFlow
from nexusmods_api.auth.sso_session import SSOSession
from nexusmods_api.errors.nexus_sso_error import NexusSSOError


class TestSSOFlow:
    """Tests `nexusmods_api.auth.sso_flow.SSOFlow`."""

    IDENTIFIER: UUID = UUID("3c4c4dd8-d76e-4b4f-999d-a14248227855")

    def test_creates_deterministic_session(self) -> None:
        """Tests construction of the documented browser authorization URL."""

        # given / when
        flow: SSOFlow = SSOFlow(SSOConfig(application_id="sse-at"))
        session: SSOSession = flow.create_session(self.IDENTIFIER)

        # then
        assert session.identifier == self.IDENTIFIER
        assert session.authorization_url == (
            f"https://www.nexusmods.com/sso?id={self.IDENTIFIER}&application=sse-at"
        )

    def test_completes_protocol_v2_and_opens_browser(
        self,
        mocker: MockerFixture,
    ) -> None:
        """Tests the documented successful synchronous SSO exchange."""

        # given
        connection: MagicMock = MagicMock()
        connection.recv.side_effect = [
            b'{"success":true,"data":{"connection_token":"resume-secret"}}',
            '{"success":true,"data":{"api_key":"issued-api-key"}}',
        ]
        context: MagicMock = mocker.patch(
            "nexusmods_api.auth.sso_flow.connect"
        ).return_value
        context.__enter__.return_value = connection
        opened_urls: list[str] = []
        flow: SSOFlow = SSOFlow(
            SSOConfig(application_id="test-application"),
            browser_opener=lambda url: not opened_urls.append(url),
        )
        session: SSOSession = flow.create_session(self.IDENTIFIER)

        # when
        auth = flow.wait_for_api_key(session)

        # then
        sent: dict[str, object] = json.loads(connection.send.call_args.args[0])
        assert sent == {
            "id": str(self.IDENTIFIER),
            "token": None,
            "protocol": 2,
        }
        assert opened_urls == [session.authorization_url]
        assert auth.headers() == {"apikey": "issued-api-key"}

    def test_rejects_error_response(self, mocker: MockerFixture) -> None:
        """Tests that structured SSO responses are treated as failures."""

        # given
        connection: MagicMock = MagicMock()
        connection.recv.return_value = '{"success":false,"data":{},"error":"denied"}'
        context: MagicMock = mocker.patch(
            "nexusmods_api.auth.sso_flow.connect"
        ).return_value
        context.__enter__.return_value = connection
        flow: SSOFlow = SSOFlow(SSOConfig(application_id="test"))

        # when / then
        with pytest.raises(NexusSSOError):
            flow.authorize(open_browser=False)

    def test_rejects_invalid_key_response_without_leaking(
        self,
        mocker: MockerFixture,
    ) -> None:
        """Tests sanitized rejection of a malformed API-key response."""

        # given
        connection: MagicMock = MagicMock()
        connection.recv.side_effect = [
            '{"success":true,"data":{"connection_token":"resume-secret"}}',
            "invalid-secret-response",
        ]
        context: MagicMock = mocker.patch(
            "nexusmods_api.auth.sso_flow.connect"
        ).return_value
        context.__enter__.return_value = connection
        flow: SSOFlow = SSOFlow(SSOConfig(application_id="test"))

        # when
        with pytest.raises(NexusSSOError) as error_info:
            flow.authorize(open_browser=False)

        # then
        assert "invalid-secret-response" not in repr(error_info.value)
        assert error_info.value.__cause__ is None

    def test_wraps_connection_timeout(self, mocker: MockerFixture) -> None:
        """Tests that connection timeouts become sanitized SSO errors."""

        # given
        mocker.patch(
            "nexusmods_api.auth.sso_flow.connect",
            side_effect=TimeoutError,
        )
        flow: SSOFlow = SSOFlow(SSOConfig(application_id="test"))

        # when / then
        with pytest.raises(NexusSSOError) as error_info:
            flow.authorize(open_browser=False)
        assert "could not be completed" in str(error_info.value)

    def test_rejects_browser_failure(self, mocker: MockerFixture) -> None:
        """Tests that a failed requested browser launch stops authorization."""

        # given
        connection: MagicMock = MagicMock()
        connection.recv.return_value = (
            '{"success":true,"data":{"connection_token":"resume-secret"}}'
        )
        context: MagicMock = mocker.patch(
            "nexusmods_api.auth.sso_flow.connect"
        ).return_value
        context.__enter__.return_value = connection
        flow: SSOFlow = SSOFlow(
            SSOConfig(application_id="test"),
            browser_opener=lambda url: False,
        )

        # when / then
        with pytest.raises(NexusSSOError, match="could not be opened"):
            flow.authorize()
