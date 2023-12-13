from __future__ import annotations

import bisect
from typing import TYPE_CHECKING, List

from prediction.models.duration import Duration

if TYPE_CHECKING:
    from prediction.models.note import Note


class Chord:
    def __init__(self, notes: List[Note]) -> None:
        assert len(notes) >= 2
        self.notes = list()
        for note in notes:
            self.add_note(note)

    @property
    def max_duration(self) -> Duration:
        return max((note.duration for note in self.notes), key=lambda d: d.raw_duration)

    @property
    def top_note(self) -> Note:
        return self.notes[-1]

    @property
    def bottom_note(self) -> Note:
        return self.notes[0]

    def is_rest(self) -> bool:
        return False

    def add_note(self, note: Note) -> None:
        self.notes.insert(
            bisect.bisect_left(self.notes, note.position.abs_position, key=lambda n: n.position.abs_position), note
        )
