from __future__ import annotations

from data.generation.models.abstract.scale import Scale
from data.generation.models.constants import ScaleIntervals, ScaleMode
from data.generation.models.note import Note


class MajorScale(Scale):
    def __init__(
        self,
        base_note: Note,
        scale_mode: ScaleMode = ScaleMode.IONIAN,
        desc: bool = False,
    ) -> None:
        self._base_note: Note = base_note
        self._intervals = ScaleIntervals.MAJOR
        self._scale_mode: ScaleMode = scale_mode
        self._desc: bool = desc
        self.notes = self._generate_notes()

    def __repr__(self) -> str:
        return " ".join(str(note).ljust(4) for note in self.notes)

    @classmethod
    def build(
        cls,
        base_note_name: str,
        scale_mode: ScaleMode = ScaleMode.IONIAN,
        desc: bool = False,
    ) -> MajorScale:
        return cls(
            Note.build_from_name(base_note_name),
            scale_mode,
            desc,
        )
