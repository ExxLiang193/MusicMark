import abc
from typing import List

from data.generation.models.note import Note


class Scale(metaclass=abc.ABCMeta):
    @property
    def notes(self) -> List[Note]:
        return self._notes

    @notes.setter
    def notes(self, value: List[Note]):
        self._notes = value

    def _generate_notes(self):
        notes = [self._base_note]
        for interval in self._intervals:
            cur_note = notes[-1]
            next_note_name = cur_note.note_name.increment()
            notes.append(
                Note.build(
                    next_note_name.name_position,
                    (cur_note.rel_position + interval - next_note_name.name_position + 6) % 12 - 6,
                )
            )
        offset = self._scale_mode.value
        if offset > 0:
            notes = notes[offset:-1] + notes[: (offset + 1)]
        return notes[::-1] if self._descending else notes