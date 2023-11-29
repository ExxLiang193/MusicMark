from typing import Dict

from data.generation.models.major_scale import MajorScale
from data.generation.models.note import Note


class BaseChord:
    def __init__(self, base_note: Note) -> None:
        self.positions: Dict[int, Note] = {1: base_note}
        self._note_bank = MajorScale(base_note).notes

    def __repr__(self) -> str:
        return str(self.positions)


# Triad Chords


class TriadChord(BaseChord):
    def __init__(self, base_note: Note) -> None:
        super(TriadChord, self).__init__(base_note)
        self.positions[3] = self._note_bank[2]
        self.positions[5] = self._note_bank[4]


class MAJ5Chord(TriadChord):
    def __init__(self, base_note: Note) -> None:
        super(MAJ5Chord, self).__init__(base_note)


class MIN5Chord(TriadChord):
    def __init__(self, base_note: Note) -> None:
        super(MIN5Chord, self).__init__(base_note)
        self.positions[3].decrement()


class DIM5Chord(TriadChord):
    def __init__(self, base_note: Note) -> None:
        super(DIM5Chord, self).__init__(base_note)
        self.positions[3].decrement()
        self.positions[5].decrement()


class AUG5Chord(TriadChord):
    def __init__(self, base_note: Note) -> None:
        super(AUG5Chord, self).__init__(base_note)
        self.positions[5].increment()


# Seventh Chords


class SeventhChord(BaseChord):
    def __init__(self, base_note: Note) -> None:
        super(SeventhChord, self).__init__(base_note)
        self.positions[3] = self._note_bank[2]
        self.positions[5] = self._note_bank[4]
        self.positions[7] = self._note_bank[6]


class MAJ7Chord(SeventhChord):
    def __init__(self, base_note: Note):
        super(MAJ7Chord, self).__init__(base_note)


class MIN7Chord(SeventhChord):
    def __init__(self, base_note: Note):
        super(MIN7Chord, self).__init__(base_note)
        self.positions[3].decrement()
        self.positions[7].decrement()


class DOM7Chord(SeventhChord):
    def __init__(self, base_note: Note):
        super(DOM7Chord, self).__init__(base_note)
        self.positions[7].decrement()


class DIM7Chord(SeventhChord):
    def __init__(self, base_note: Note):
        super(DIM7Chord, self).__init__(base_note)
        self.positions[3].decrement()
        self.positions[5].decrement()
        self.positions[7].decrement(2)


class HalfDIM7Chord(SeventhChord):
    def __init__(self, base_note: Note) -> None:
        super(HalfDIM7Chord, self).__init__(base_note)
        self.positions[3].decrement()
        self.positions[5].decrement()
        self.positions[7].decrement()


class MINMAJ7Chord(SeventhChord):
    def __init__(self, base_note: Note) -> None:
        super(MINMAJ7Chord, self).__init__(base_note)
        self.positions[3].decrement()


class AUGMAJ7Chord(SeventhChord):
    def __init__(self, base_note: Note) -> None:
        super(AUGMAJ7Chord, self).__init__(base_note)
        self.positions[5].increment()
