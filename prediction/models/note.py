from __future__ import annotations

from decimal import Decimal
from typing import Optional

from prediction.models.duration import Duration
from prediction.models.position import Position


class Note:
    def __init__(self, position: Optional[Position], duration: Duration, tied: bool = False) -> None:
        self.position: Optional[Position] = position
        self.duration: Duration = duration
        self._tied: bool = tied

    def __repr__(self) -> str:
        note_name: str = "Rest" if self.is_rest() else "Note"
        tie_symbol: str = "~" if self._tied else ""
        return f"{note_name}({self.position}{{{tie_symbol}{self.duration}}})"

    def __hash__(self) -> int:
        return hash(repr(self))

    def is_rest(self) -> bool:
        return self.position is None

    def is_held(self) -> bool:
        return self._tied

    def extend_duration(self, other: Note) -> None:
        assert self.position == other.position
        self.duration += other.duration

    def is_tagged(self):
        return hasattr(self, "ids")

    @classmethod
    def from_raw(cls, abs_position: Optional[int], raw_duration: Decimal, tied: bool = False) -> Note:
        return cls(None if abs_position is None else Position(abs_position), Duration(raw_duration), tied)
