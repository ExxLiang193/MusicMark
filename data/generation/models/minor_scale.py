from __future__ import annotations

from data.generation.models.abstract.scale import Scale
from data.generation.models.alter import Alter
from data.generation.models.constants import ScaleMode, ScaleType
from data.generation.models.note import Note
from data.generation.models.note_name import NoteName


class MinorScale(Scale):
    NATURAL_INTERVALS = (2, 1, 2, 2, 1, 2, 2)
    HARMONIC_INTERVALS = (2, 1, 2, 2, 1, 3, 1)
    MELODIC_INTERVALS = (2, 1, 2, 2, 2, 2, 1)

    def __init__(
        self,
        base_note: Note,
        scale_type: ScaleType = ScaleType.NATURAL,
        scale_mode: ScaleMode = ScaleMode.IONIAN,
        desc: bool = False,
    ) -> None:
        self._base_note: Note = base_note
        self._intervals = self._get_intervals(scale_type)
        self._scale_mode: ScaleMode = scale_mode
        self._descending: bool = desc
        self.notes = self._generate_notes()

    def __repr__(self) -> str:
        return " ".join(str(note).ljust(3) for note in self.notes)

    def _get_intervals(self, scale_type: ScaleType):
        if scale_type == ScaleType.HARMONIC:
            return self.HARMONIC_INTERVALS
        elif scale_type == ScaleType.MELODIC:
            return self.MELODIC_INTERVALS
        return self.NATURAL_INTERVALS

    @classmethod
    def build(cls, base_note_name: str, *args, **kwargs) -> MinorScale:
        return cls(
            Note(NoteName.build(base_note_name[0]), Alter.build(base_note_name[1:])),
            *args,
            **kwargs,
        )
