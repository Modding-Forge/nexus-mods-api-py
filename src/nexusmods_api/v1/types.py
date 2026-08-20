"""Copyright (c) Modding Forge."""

from typing import Literal, TypeAlias

UpdatePeriod: TypeAlias = Literal["1d", "1w", "1m"]
EndorsementStatus: TypeAlias = Literal["endorse", "abstain"]
Changelogs: TypeAlias = dict[str, list[str]]
