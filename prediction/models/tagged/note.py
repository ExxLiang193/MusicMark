from __future__ import annotations

from decimal import Decimal
from typing import List, Optional

from prediction.models.duration import Duration
from prediction.models.note import Note
from prediction.models.position import Position


class TaggedNote(Note):
    def __init__(self, position: Optional[Position], duration: Duration, ids: List[int], tied: bool = False) -> None:
        super().__init__(position, duration, tied)
        self.ids: List[int] = ids
        self._fingering: int | None = None

    @property
    def fingering(self) -> int:
        return self._fingering

    @fingering.setter
    def fingering(self, value: int) -> None:
        assert 1 <= value <= 5, str(value)
        self._fingering: int = value

    def __repr__(self) -> str:
        note_name: str = "TaggedRest" if self.is_rest() else "TaggedNote"
        tie_symbol: str = "~" if self._tied else ""
        return f"{note_name}({self.position}{{{tie_symbol}{self.duration}}})@{self.ids}"

    @classmethod
    def from_raw(cls, abs_position: Optional[int], raw_duration: Decimal, ids: List[int], tied: bool = False) -> Note:
        return cls(None if abs_position is None else Position(abs_position), Duration(raw_duration), ids, tied)

    def extend_duration(self, other: TaggedNote) -> None:
        assert self.position == other.position
        self.duration += other.duration
        self.ids.extend(other.ids)
