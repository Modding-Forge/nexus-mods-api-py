"""Copyright (c) Modding Forge."""

from collections.abc import Awaitable, Callable
from typing import Optional, TypeAlias, TypeAliasType

JsonValue = TypeAliasType(
    "JsonValue",
    Optional[str | int | float | bool | list["JsonValue"] | dict[str, "JsonValue"]],
)
QueryParameters: TypeAlias = dict[str, str | int | float | bool]
AsyncSleepCallback: TypeAlias = Callable[[float], Awaitable[None]]
SleepCallback: TypeAlias = Callable[[float], None]
