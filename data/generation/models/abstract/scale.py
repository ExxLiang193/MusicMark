from __future__ import annotations
import abc
from typing import List

from data.generation.models.note import Note
from data.generation.models.interval import Interval


class Scale(metaclass=abc.ABCMeta):
    @property
    def notes(self) -> List[Note]:
        return self._notes

    @notes.setter
    def notes(self, value: List[Note]):
        self._notes = value

    @property
    def intervals(self) -> List[Interval]:
        return self._intervals

    @intervals.setter
    def intervals(self, value: List[Interval]):
        self._intervals = value

    def _generate_notes(self, rh: bool) -> List[Note]:
        notes = [self._base_note]
        for interval in self.intervals:
            cur_note = notes[-1]
            next_note_name = cur_note.note_name.increment() if rh else cur_note.note_name.decrement()
            notes.append(
                Note.build_from_raw(
                    next_note_name.name_position,
                    (cur_note.rel_position + interval - next_note_name.name_position + 6) % 12 - 6,
                )
            )
        offset = self._scale_mode.value if rh else (-self._scale_mode.value) % 7
        if offset > 0:
            notes = notes[offset:-1] + notes[: offset + 1]
            self.intervals = self.intervals[offset:] + self.intervals[:offset]
        return notes
