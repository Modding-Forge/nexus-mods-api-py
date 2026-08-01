"""Copyright (c) Modding Forge."""

import json
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID

import pytest
from pytest_mock import MockerFixture

from nexusmods_api.auth.async_sso_flow import AsyncSSOFlow
from nexusmods_api.auth.sso_config import SSOConfig
from nexusmods_api.auth.sso_session import SSOSession
from nexusmods_api.errors.nexus_sso_error import NexusSSOError


class TestAsyncSSOFlow:
    """Tests `nexusmods_api.auth.async_sso_flow.AsyncSSOFlow`."""

    IDENTIFIER: UUID = UUID("a4dd740f-1044-4619-b99c-7e76f7461acd")

    async def test_receives_key_without_opening_browser(
        self,
        mocker: MockerFixture,
    ) -> None:
        """Tests the documented successful asynchronous SSO exchange."""

        # given
        connection: MagicMock = MagicMock()
        connection.send = AsyncMock()
        connection.recv = AsyncMock(return_value="async-api-key")
        context: MagicMock = mocker.patch(
            "nexusmods_api.auth.async_sso_flow.connect"
        ).return_value
        context.__aenter__ = AsyncMock(return_value=connection)
        context.__aexit__ = AsyncMock(return_value=None)
        flow: AsyncSSOFlow = AsyncSSOFlow(SSOConfig(application_id="async-test"))
        session: SSOSession = flow.create_session(self.IDENTIFIER)

        # when
        auth = await flow.wait_for_api_key(session, open_browser=False)

        # then
        sent: dict[str, str] = json.loads(connection.send.call_args.args[0])
        assert sent["id"] == str(self.IDENTIFIER)
        assert sent["appid"] == "async-test"
        assert auth.headers() == {"apikey": "async-api-key"}

    async def test_wraps_async_timeout(self, mocker: MockerFixture) -> None:
        """Tests that asynchronous timeouts become sanitized SSO errors."""

        # given
        connection: MagicMock = MagicMock()
        connection.send = AsyncMock()
        connection.recv = AsyncMock(side_effect=TimeoutError)
        context: MagicMock = mocker.patch(
            "nexusmods_api.auth.async_sso_flow.connect"
        ).return_value
        context.__aenter__ = AsyncMock(return_value=connection)
        context.__aexit__ = AsyncMock(return_value=None)
        flow: AsyncSSOFlow = AsyncSSOFlow(SSOConfig(application_id="test"))

        # when / then
        with pytest.raises(NexusSSOError, match="could not be completed"):
            await flow.authorize(open_browser=False)

    async def test_rejects_browser_failure(self, mocker: MockerFixture) -> None:
        """Tests that asynchronous browser launch failure is reported."""

        # given
        connection: MagicMock = MagicMock()
        connection.send = AsyncMock()
        context: MagicMock = mocker.patch(
            "nexusmods_api.auth.async_sso_flow.connect"
        ).return_value
        context.__aenter__ = AsyncMock(return_value=connection)
        context.__aexit__ = AsyncMock(return_value=None)
        flow: AsyncSSOFlow = AsyncSSOFlow(
            SSOConfig(application_id="test"),
            browser_opener=lambda url: False,
        )

        # when / then
        with pytest.raises(NexusSSOError, match="could not be opened"):
            await flow.authorize()
