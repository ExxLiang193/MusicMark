from __future__ import annotations

import sys
from typing import List, Tuple

from data.generation.models.interval import Interval
from data.generation.models.note import Note


class AnnotatedNoteSequence:
    def __init__(
        self, notes: List[Note], fingerings: List[int], intervals: Tuple[Interval, ...], infer_fingerings: bool = True
    ) -> None:
        assert len(fingerings) == len(notes)
        assert len(intervals) == len(notes) - 1
        self.notes: List[Note] = notes
        self.fingerings: List[int] = fingerings
        self.intervals: Tuple[Interval, ...] = intervals
        self._infer_fingerings: bool = infer_fingerings

    def __eq__(self, other: AnnotatedNoteSequence) -> bool:
        return self.notes == other.notes and self.fingerings == other.fingerings and self.intervals == other.intervals

    def __hash__(self) -> int:
        note_fingerings = (f"{note.rel_position},{fingering}" for note, fingering in zip(self.notes, self.fingerings))
        self_str = f"{next(note_fingerings)} " + " ".join(
            f"<{interval}> {note_fingering}" for note_fingering, interval in zip(note_fingerings, self.intervals)
        )
        return hash(self_str)

    def __repr__(self) -> str:
        note_fingerings = (f"({note},{fingering})" for note, fingering in zip(self.notes, self.fingerings))
        return f"{next(note_fingerings)} " + " ".join(
            f"<{interval}> {note_fingering}" for note_fingering, interval in zip(note_fingerings, self.intervals)
        )

    def __getitem__(self, idx: slice) -> AnnotatedNoteSequence:
        safe_start, safe_stop = (idx.start or 0, idx.stop or sys.maxsize)
        return AnnotatedNoteSequence(
            self.notes[idx],
            self.fingerings[idx],
            self.intervals[max(0, safe_start) : safe_stop - 1],
        )

    def __add__(self, other: AnnotatedNoteSequence) -> AnnotatedNoteSequence:
        assert self.notes[-1] == other.notes[0]
        new_fingerings = self.fingerings + other.fingerings[1:]
        # If the intervals change directions (notes create a local max/min)
        # if self._infer_fingerings and self.intervals[-1].value * other.intervals[0].value < 0:
        #     new_fingerings[len(self.fingerings) - 1] = new_fingerings[len(self.fingerings) - 2] + (
        #         1 if self.intervals[-1].value >= 0 else -1
        #     )
        return AnnotatedNoteSequence(self.notes + other.notes[1:], new_fingerings, self.intervals + other.intervals)

    def __mul__(self, amount: int) -> AnnotatedNoteSequence:
        result = self
        for _ in range(amount - 1):
            result += result
        return result

    def __len__(self) -> int:
        return len(self.notes)

    @property
    def reverse(self) -> AnnotatedNoteSequence:
        return AnnotatedNoteSequence(
            self.notes[::-1], self.fingerings[::-1], tuple(interval.inverse for interval in self.intervals)[::-1]
        )
