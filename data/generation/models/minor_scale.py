from __future__ import annotations

from typing import List, Tuple

from data.generation.models.abstract.scale import Scale
from data.generation.models.constants import ScaleIntervals, ScaleMode, ScaleType
from data.generation.models.interval import Interval
from data.generation.models.note import Note


class MinorScale(Scale):
    def __init__(
        self,
        base_note: Note,
        scale_type: ScaleType = ScaleType.NATURAL,
        scale_mode: ScaleMode = ScaleMode.IONIAN,
    ) -> None:
        self._base_note: Note = base_note
        self._scale_type: ScaleType = scale_type
        self._scale_mode: ScaleMode = scale_mode
        self.intervals: Tuple[Interval, ...] = self._get_intervals(scale_type)
        self.notes: List[Note] = self._generate_notes()

    def __repr__(self) -> str:
        return " ".join(str(note).ljust(4) for note in self.notes)

    def _get_intervals(self, scale_type: ScaleType):
        if scale_type == ScaleType.HARMONIC:
            return ScaleIntervals.MINOR_HARMONIC
        elif scale_type == ScaleType.MELODIC:
            return ScaleIntervals.MINOR_MELODIC
        return ScaleIntervals.MINOR_NATURAL

    @classmethod
    def build(
        cls,
        base_note_name: str,
        scale_type: ScaleType = ScaleType.NATURAL,
        scale_mode: ScaleMode = ScaleMode.IONIAN,
    ) -> MinorScale:
        return cls(
            Note.build_from_name(base_note_name),
            scale_type,
            scale_mode,
        )
