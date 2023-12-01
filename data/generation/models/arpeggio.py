from __future__ import annotations

from itertools import chain
from typing import List, Tuple, Type

from data.generation.models.chords import BaseChord, SeventhChord, TriadChord
from data.generation.models.constants import Inversion
from data.generation.models.interval import Interval
from data.generation.models.note import Note


class Arpeggio:
    TRIAD_POSITIONS = (1, 3, 5, 1)
    SEVENTH_POSITIONS = (1, 3, 5, 7, 1)

    def __init__(
        self,
        ref_chord: BaseChord,
        inversion: Inversion = Inversion.ROOT,
        alternating: bool = False,
    ) -> None:
        self._ref_chord: BaseChord = ref_chord
        self._inversion: Inversion = inversion
        self._alternating: bool = alternating
        self.notes, self.intervals = self._generate_notes(ref_chord)

    def __repr__(self) -> str:
        return " ".join(str(note).ljust(4) for note in self.notes)

    def _generate_notes(self, ref_chord: BaseChord) -> Tuple[List[Note], Tuple[Interval, ...]]:
        if isinstance(ref_chord, TriadChord):
            positions = self.TRIAD_POSITIONS
        elif isinstance(ref_chord, SeventhChord):
            positions = self.SEVENTH_POSITIONS

        notes: List[Note] = [ref_chord.positions[position] for position in positions]
        intervals: Tuple[Interval, ...] = tuple(
            (ref_chord.intervals[positions[i + 1]] - ref_chord.intervals[positions[i]]) % 12
            for i in range(len(positions) - 1)
        )

        if self._inversion.value > 0:
            notes = notes[self._inversion.value : -1] + notes[: self._inversion.value + 1]
            intervals = intervals[self._inversion.value :] + intervals[: self._inversion.value]
        return notes, intervals

    @classmethod
    def build(
        cls,
        base_note_name: str,
        chord_class: Type[BaseChord],
        inversion: Inversion = Inversion.ROOT,
        alternating: bool = False,
    ) -> Arpeggio:
        return cls(
            chord_class(Note.build_from_name(base_note_name)),
            inversion,
            alternating,
        )
