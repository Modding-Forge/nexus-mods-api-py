"""Copyright (c) Modding Forge."""

import pytest
from pydantic import ValidationError

from nexusmods_api.models.nexus_model import NexusModel
from nexusmods_api.models.request_model import RequestModel


class TestNexusModel:
    """Tests the shared Nexus Mods model policies."""

    def test_response_model_accepts_additive_fields(self) -> None:
        """Tests that response models preserve unknown upstream fields."""

        # given
        payload: dict[str, object] = {"new_field": "value"}

        # when
        model: NexusModel = NexusModel.model_validate(payload)

        # then
        assert model.model_extra == payload

    def test_response_model_is_frozen(self) -> None:
        """Tests that response models cannot be mutated."""

        # given / when
        model: NexusModel = NexusModel()

        # then
        assert model.model_config.get("frozen") is True

    def test_request_model_rejects_unknown_fields(self) -> None:
        """Tests that request models reject misspelled input fields."""

        # given
        payload: dict[str, object] = {"unknown": "value"}

        # when / then
        with pytest.raises(ValidationError):
            RequestModel.model_validate(payload)
