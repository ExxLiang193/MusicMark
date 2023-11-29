from __future__ import annotations

from data.generation.models.note_name import NoteName
from data.generation.models.alter import Alter


class Note:
    def __init__(self, note_name: NoteName, alter: Alter) -> None:
        self.note_name: NoteName = note_name
        self.alter: Alter = alter

    def __repr__(self) -> str:
        return self.note_name.name + self.alter.symbol

    @property
    def name(self):
        return self.note_name.name

    @property
    def rel_position(self):
        return self.note_name.name_position + self.alter._value

    def is_black_key(self):
        return self.rel_position in NoteName.BLACK_POSITIONS

    @classmethod
    def build(cls, rel_position: int, alter_value: int) -> Note:
        return cls(NoteName(rel_position), Alter(alter_value))