from __future__ import annotations
from data.generation.models.interval import Interval

from data.generation.models.note_name import NoteName
from data.generation.models.alter import Alter


class Note:
    def __init__(self, note_name: NoteName, alter: Alter) -> None:
        self.note_name: NoteName = note_name
        self.alter: Alter = alter

    def __hash__(self) -> int:
        return hash(self.rel_position)

    def __repr__(self) -> str:
        return self.note_name.name + self.alter.symbol

    def __eq__(self, other: Note) -> bool:
        return self.rel_position == other.rel_position

    @property
    def name(self) -> str:
        return self.note_name.name

    @property
    def rel_position(self) -> int:
        return (self.note_name.name_position + self.alter._value) % 12

    def is_black_key(self) -> bool:
        return self.rel_position in NoteName.BLACK_POSITIONS

    def raise_(self, amount: int = 1) -> None:
        self.alter.increment(amount)

    def lower_(self, amount: int = 1) -> None:
        self.alter.decrement(amount)

    def __add__(self, interval: Interval) -> None:
        for _ in range(1, abs(interval.value) + 1):
            if interval.value >= 0:
                self.raise_(1)
                if self.rel_position == self.note_name.increment().name_position:
                    self.note_name.increment(in_place=True)
                    self.alter = Alter(0)
            else:
                self.lower_(1)
                if self.rel_position == self.note_name.decrement().name_position:
                    self.note_name.decrement(in_place=True)
                    self.alter = Alter(0)
        return self

    @classmethod
    def build_from_raw(cls, rel_position: int, alter_value: int) -> Note:
        return cls(NoteName(rel_position), Alter(alter_value))

    @classmethod
    def build_from_name(cls, base_note_name: str) -> Note:
        return cls(NoteName.build(base_note_name[0]), Alter.build(base_note_name[1:]))
