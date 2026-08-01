"""Copyright (c) Modding Forge."""

from typing import Self

from pydantic import ConfigDict, Field, SecretStr

from ..models.request_model import RequestModel


class ApiKeyAuth(RequestModel):
    """Provides manual application-specific API-key authentication."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        populate_by_name=True,
        use_attribute_docstrings=True,
    )

    api_key: SecretStr = Field(min_length=1, repr=False)
    """The application-specific personal Nexus Mods API key."""

    @classmethod
    def from_value(cls, api_key: str) -> Self:
        """Creates authentication from a raw key at the application boundary.

        Args:
            api_key (str): Application-specific personal Nexus Mods API key.

        Returns:
            Self: Masked API-key authentication data.
        """

        return cls(api_key=SecretStr(api_key))

    def headers(self) -> dict[str, str]:
        """Builds the HTTP authentication headers.

        Returns:
            dict[str, str]: A new mapping containing the API-key header.
        """

        return {"apikey": self.api_key.get_secret_value()}
