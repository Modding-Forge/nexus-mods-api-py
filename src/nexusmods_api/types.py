"""Copyright (c) Modding Forge."""

from collections.abc import Callable
from typing import Optional

type JsonValue = Optional[
    str | int | float | bool | list["JsonValue"] | dict[str, "JsonValue"]
]
type QueryParameters = dict[str, str | int | float | bool]
type SleepCallback = Callable[[float], None]
