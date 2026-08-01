"""Copyright (c) Modding Forge."""

from typing import Literal

type UpdatePeriod = Literal["1d", "1w", "1m"]
type EndorsementStatus = Literal["endorse", "abstain"]
type Changelogs = dict[str, list[str]]
