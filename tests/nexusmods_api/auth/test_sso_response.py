"""Copyright (c) Modding Forge."""

from nexusmods_api.auth.sso_response import SSOResponse


class TestSSOResponse:
    """Tests secret handling in structured SSO protocol responses."""

    def test_masks_protocol_secrets(self) -> None:
        """Tests that protocol response representations cannot expose secrets."""

        # given
        connection_token: str = "connection-token-secret"
        api_key: str = "api-key-secret"

        # when
        response: SSOResponse = SSOResponse.model_validate(
            {
                "success": True,
                "data": {
                    "connection_token": connection_token,
                    "api_key": api_key,
                },
            }
        )

        # then
        representation: str = repr(response)
        assert connection_token not in representation
        assert api_key not in representation
