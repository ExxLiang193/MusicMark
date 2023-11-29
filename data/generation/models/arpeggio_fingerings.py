from __future__ import annotations

from typing import Tuple

from data.generation.models.arpeggio import Arpeggio
from data.generation.models.chords import TriadChord, SeventhChord


class ArpeggioFingerings:
    TRIAD_SEQUENCE_1 = (1, 2, 3)
    TRIAD_SEQUENCE_2 = (1, 2, 4)
    SEVENTH_SEQUENCE = (1, 2, 3, 4)

    def __init__(self, fingerings: Tuple[int, ...]) -> None:
        self.values: Tuple[int, ...] = fingerings

    def __repr__(self) -> str:
        return str(self.values)

    @classmethod
    def build(cls, arpeggio: Arpeggio) -> ArpeggioFingerings:
        note_idx = iter(range(len(arpeggio.notes)))
        first_white = next((i for i in note_idx if not arpeggio.notes[i].is_black_key()), float("inf"))
        if isinstance(arpeggio._ref_chord, TriadChord) and (
            (not arpeggio._ref_chord.positions[1].is_black_key()) or first_white == float("inf")
        ):
            target_sequence = cls.TRIAD_SEQUENCE_1
        elif isinstance(arpeggio._ref_chord, TriadChord):
            target_sequence = cls.TRIAD_SEQUENCE_2
        elif isinstance(arpeggio._ref_chord, SeventhChord):
            target_sequence = cls.SEVENTH_SEQUENCE
        fingerings = target_sequence[0 if first_white == float("inf") else -first_white :]
        fingerings += target_sequence[: len(arpeggio.notes) - len(fingerings)]
        return cls(fingerings)
