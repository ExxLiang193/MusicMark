from __future__ import annotations

from typing import List, Tuple

from data.generation.models.abstract.scale import Scale
from data.generation.models.constants import ScaleIntervals, ScaleMode
from data.generation.models.interval import Interval
from data.generation.models.note import Note


class MajorScale(Scale):
    def __init__(
        self,
        base_note: Note,
        scale_mode: ScaleMode = ScaleMode.IONIAN,
    ) -> None:
        self._base_note: Note = base_note
        self._scale_mode: ScaleMode = scale_mode
        self.intervals: Tuple[Interval, ...] = ScaleIntervals.MAJOR
        self.notes: List[Note] = self._generate_notes()

    def __repr__(self) -> str:
        return " ".join(str(note).ljust(4) for note in self.notes)

    @classmethod
    def build(
        cls,
        base_note_name: str,
        scale_mode: ScaleMode = ScaleMode.IONIAN,
    ) -> MajorScale:
        return cls(
            Note.build_from_name(base_note_name),
            scale_mode,
        )
