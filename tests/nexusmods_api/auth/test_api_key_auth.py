"""Copyright (c) Modding Forge."""

from nexusmods_api.auth.api_key_auth import ApiKeyAuth


class TestApiKeyAuth:
    """Tests `nexusmods_api.auth.api_key_auth.ApiKeyAuth`."""

    API_KEY: str = "application-specific-secret"

    def test_builds_api_key_header(self) -> None:
        """Tests that the raw key is available only in an explicit header."""

        # given
        auth: ApiKeyAuth = ApiKeyAuth.from_value(self.API_KEY)

        # when
        headers: dict[str, str] = auth.headers()

        # then
        assert headers == {"apikey": self.API_KEY}

    def test_masks_key_in_representations(self) -> None:
        """Tests that common model representations do not expose the key."""

        # given
        auth: ApiKeyAuth = ApiKeyAuth.from_value(self.API_KEY)

        # when
        representation: str = repr(auth)
        serialized: str = auth.model_dump_json()

        # then
        assert self.API_KEY not in representation
        assert self.API_KEY not in serialized
