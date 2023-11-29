from __future__ import annotations

from typing import Type

from data.generation.models.chords import BaseChord, TriadChord, SeventhChord
from data.generation.models.note import Note
from data.generation.models.constants import Inversion

from typing import Tuple
from itertools import chain


class Arpeggio:
    def __init__(
        self, ref_chord: BaseChord, inversion: Inversion = Inversion.ROOT, alternating: bool = False, desc: bool = False
    ) -> None:
        self._ref_chord: BaseChord = ref_chord
        self._inversion: Inversion = inversion
        self._alternating: bool = alternating
        self._desc: bool = desc
        self.notes = self._generate_notes(ref_chord)

    def __repr__(self) -> str:
        return " ".join(str(note).ljust(4) for note in self.notes)

    def _generate_notes(self, ref_chord: BaseChord):
        def transform(notes: Tuple[int, ...]) -> Tuple[int, ...]:
            if self._inversion.value > 0:
                notes = notes[self._inversion.value :] + notes[: self._inversion.value]
            if self._alternating:
                notes = tuple(notes[i] for i in chain(range(0, len(notes), 2), range(1, len(notes), 2)))
            notes += (notes[0],)
            return notes[::-1] if self._desc else notes

        if isinstance(ref_chord, TriadChord):
            return transform((ref_chord.positions[1], ref_chord.positions[3], ref_chord.positions[5]))
        elif isinstance(ref_chord, SeventhChord):
            return transform(
                (ref_chord.positions[1], ref_chord.positions[3], ref_chord.positions[5], ref_chord.positions[7])
            )

    @classmethod
    def build(
        cls,
        base_note_name: str,
        chord_class: Type[BaseChord],
        inversion: Inversion = Inversion.ROOT,
        alternating: bool = False,
        desc: bool = False,
    ) -> Arpeggio:
        return cls(
            chord_class(Note.build_from_name(base_note_name)),
            inversion,
            alternating,
            desc,
        )
