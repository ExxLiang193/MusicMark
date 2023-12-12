from __future__ import annotations

from typing import List, Tuple, Type

from data.generation.models.chords import BaseChord, SeventhChord, TriadChord
from data.generation.models.constants import Inversion
from data.generation.models.interval import Interval
from data.generation.models.note import Note


class Arpeggio:
    TRIAD_POSITIONS = (1, 3, 5, 8)
    SEVENTH_POSITIONS = (1, 3, 5, 7, 8)

    def __init__(
        self,
        ref_chord: BaseChord,
        inversion: Inversion = Inversion.ROOT,
        rh: bool = True,
    ) -> None:
        self._ref_chord: BaseChord = ref_chord
        self._inversion: Inversion = inversion
        self.notes, self.intervals = self._generate_notes(ref_chord, rh)

    def __repr__(self) -> str:
        return " ".join(str(note).ljust(4) for note in self.notes)

    def _generate_notes(self, ref_chord: BaseChord, rh: bool) -> Tuple[List[Note], Tuple[Interval, ...]]:
        if isinstance(ref_chord, TriadChord):
            positions = self.TRIAD_POSITIONS
        elif isinstance(ref_chord, SeventhChord):
            positions = self.SEVENTH_POSITIONS
        positions = positions if rh else positions[::-1]

        notes: List[Note] = [ref_chord.positions[position] for position in positions]
        intervals: Tuple[Interval, ...] = tuple(
            ref_chord.intervals[positions[i + 1]] - ref_chord.intervals[positions[i]] for i in range(len(positions) - 1)
        )

        offset = self._inversion.value if rh else (-self._inversion.value) % (len(positions) - 1)
        if offset > 0:
            notes = notes[offset:-1] + notes[: offset + 1]
            intervals = intervals[offset:] + intervals[:offset]
        return notes, intervals

    @classmethod
    def build(
        cls,
        base_note_name: str,
        chord_class: Type[BaseChord],
        inversion: Inversion = Inversion.ROOT,
        rh: bool = True,
    ) -> Arpeggio:
        return cls(
            chord_class(Note.build_from_name(base_note_name)),
            inversion,
            rh,
        )
