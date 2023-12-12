from typing import Dict, Final
from data.generation.models.abstract.scale import Scale

from data.generation.models.interval import Interval
from data.generation.models.major_scale import MajorScale
from data.generation.models.note import Note


class BaseChord:
    def __init__(self, base_note: Note) -> None:
        self.positions: Dict[int, Note] = dict()
        self.intervals: Dict[int, Interval] = dict()
        self._ref_scale: Scale = MajorScale(base_note)
        self._add_note(position=1)
        self._add_note(position=8)

    def _add_note(self, position: int) -> None:
        self.positions[position] = self._ref_scale.notes[position - 1]
        self.intervals[position] = Interval(sum(self._ref_scale.intervals[: position - 1]))

    def _adjust_note(self, position: int, delta: int) -> None:
        if delta > 0:
            self.positions[position].raise_(delta)
        elif delta < 0:
            self.positions[position].lower_(abs(delta))
        self.intervals[position] += delta

    def __repr__(self) -> str:
        return str(self.positions)


# Triad Chords


class TriadChord(BaseChord):
    def __init__(self, base_note: Note) -> None:
        super(TriadChord, self).__init__(base_note)
        self._add_note(position=3)
        self._add_note(position=5)


class MAJ5Chord(TriadChord):
    def __init__(self, base_note: Note) -> None:
        super(MAJ5Chord, self).__init__(base_note)


class MIN5Chord(TriadChord):
    def __init__(self, base_note: Note) -> None:
        super(MIN5Chord, self).__init__(base_note)
        self._adjust_note(position=3, delta=-1)


class DIM5Chord(TriadChord):
    def __init__(self, base_note: Note) -> None:
        super(DIM5Chord, self).__init__(base_note)
        self._adjust_note(position=3, delta=-1)
        self._adjust_note(position=5, delta=-1)


class AUG5Chord(TriadChord):
    def __init__(self, base_note: Note) -> None:
        super(AUG5Chord, self).__init__(base_note)
        self._adjust_note(position=5, delta=1)


# Seventh Chords


class SeventhChord(BaseChord):
    def __init__(self, base_note: Note) -> None:
        super(SeventhChord, self).__init__(base_note)
        self._add_note(position=3)
        self._add_note(position=5)
        self._add_note(position=7)


class MAJ7Chord(SeventhChord):
    def __init__(self, base_note: Note):
        super(MAJ7Chord, self).__init__(base_note)


class MIN7Chord(SeventhChord):
    def __init__(self, base_note: Note):
        super(MIN7Chord, self).__init__(base_note)
        self._adjust_note(position=3, delta=-1)
        self._adjust_note(position=7, delta=-1)


class DOM7Chord(SeventhChord):
    def __init__(self, base_note: Note):
        super(DOM7Chord, self).__init__(base_note)
        self._adjust_note(position=7, delta=-1)


class DIM7Chord(SeventhChord):
    def __init__(self, base_note: Note):
        super(DIM7Chord, self).__init__(base_note)
        self._adjust_note(position=3, delta=-1)
        self._adjust_note(position=5, delta=-1)
        self._adjust_note(position=7, delta=-2)


class HalfDIM7Chord(SeventhChord):
    def __init__(self, base_note: Note) -> None:
        super(HalfDIM7Chord, self).__init__(base_note)
        self._adjust_note(position=3, delta=-1)
        self._adjust_note(position=5, delta=-1)
        self._adjust_note(position=7, delta=-1)


class MINMAJ7Chord(SeventhChord):
    def __init__(self, base_note: Note) -> None:
        super(MINMAJ7Chord, self).__init__(base_note)
        self._adjust_note(position=3, delta=-1)


class AUGMAJ7Chord(SeventhChord):
    def __init__(self, base_note: Note) -> None:
        super(AUGMAJ7Chord, self).__init__(base_note)
        self._adjust_note(position=5, delta=1)


TRIAD_CHORD_CLASSES: Final[BaseChord] = (
    MAJ5Chord,
    MIN5Chord,
    DIM5Chord,
    AUG5Chord,
)
SEVENTH_CHORD_CLASSES: Final[BaseChord] = (
    MAJ7Chord,
    MIN7Chord,
    DOM7Chord,
    DIM7Chord,
    HalfDIM7Chord,
    MINMAJ7Chord,
    AUGMAJ7Chord,
)
