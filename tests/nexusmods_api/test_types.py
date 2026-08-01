"""Copyright (c) Modding Forge."""

from pydantic import TypeAdapter

from nexusmods_api.types import JsonValue


class TestJsonValue:
    """Tests the recursive JSON value type alias."""

    def test_validates_nested_json(self) -> None:
        """Tests that nested JSON structures validate without losing values."""

        # given
        payload: dict[str, object] = {
            "items": [1, "two", True, None, {"nested": 3.0}],
        }
        adapter: TypeAdapter[JsonValue] = TypeAdapter(JsonValue)

        # when
        result: JsonValue = adapter.validate_python(payload)

        # then
        assert result == payload
