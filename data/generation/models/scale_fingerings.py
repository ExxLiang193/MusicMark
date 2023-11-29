from __future__ import annotations

from typing import Tuple

from data.generation.models.abstract.scale import Scale


class ScaleFingerings:
    SEQUENCES = {1: (1, 2, 3), 2: (1, 2, 3, 4)}
    SWAP_MASK = int("11", base=2)
    SCALE_LENGTH = 8

    def __init__(self, fingerings: Tuple[int, ...]) -> None:
        self.values: Tuple[int, ...] = fingerings

    def __repr__(self) -> str:
        return str(self.values)

    @classmethod
    def build(cls, scale: Scale) -> ScaleFingerings:
        note_idx = iter(range(len(scale.notes)))
        # Get seq index of first white key
        first_white = next(i for i in note_idx if not scale.notes[i].is_black_key())
        # Ignore the next black keys until next white key
        next((i for i in note_idx if scale.notes[i].is_black_key()), float("inf"))
        # Get seq index of second white key
        second_white = next((i for i in note_idx if not scale.notes[i].is_black_key()), float("inf"))
        init_sequence_idx = 2 if second_white - first_white == 4 else 1
        init_sequence_idx = init_sequence_idx ^ cls.SWAP_MASK if scale.notes[0].is_black_key() else init_sequence_idx
        init_sequence = cls.SEQUENCES[init_sequence_idx]
        start_finger_idx = (len(init_sequence) - first_white) % len(init_sequence)
        fingerings = init_sequence[start_finger_idx:] + cls.SEQUENCES[init_sequence_idx ^ cls.SWAP_MASK]
        fingerings += init_sequence[: (cls.SCALE_LENGTH - len(fingerings))]
        return cls(fingerings)
