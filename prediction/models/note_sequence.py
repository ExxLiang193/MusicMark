from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING, List, Optional, Union

from prediction.models.chord import Chord
from prediction.models.note import Note
from prediction.models.position import Position

if TYPE_CHECKING:
    from prediction.models.duration import Duration
    from prediction.models.interval import Interval


class NoteSequence:
    def __init__(self, notes: List[Union[Note, Chord]] = None) -> None:
        self.notes: List[Union[Note, Chord]] = notes or list()

    def __getitem__(self, idx) -> NoteSequence:
        return NoteSequence(self.notes[idx])

    def __len__(self) -> int:
        return len(self.notes)

    def __add__(self, other: NoteSequence) -> NoteSequence:
        return NoteSequence(self.notes + other.notes)

    @property
    def first_note(self) -> Note:
        return next(note for note in self.notes if not note.is_rest())

    @property
    def last_note(self) -> Note:
        return next(note for note in reversed(self.notes) if not note.is_rest())

    @property
    def intervals(self) -> List[Optional[Interval]]:
        if any(isinstance(element, Chord) for element in self.notes):
            raise Exception("Cannot extract intervals between chords and notes.")

        def parse(left_note: Union[Note, Chord], right_note: Union[Note, Chord]) -> Optional[Interval]:
            if left_note.is_rest() or right_note.is_rest():
                return None
            return right_note.position - left_note.position

        return [parse(self.notes[i - 1], self.notes[i]) for i in range(1, len(self.notes))]

    @property
    def durations(self) -> List[Duration]:
        if any(isinstance(element, Chord) for element in self.notes):
            raise Exception("Cannot extract durations between chords and notes.")
        return [note.duration for note in self.notes]

    @property
    def positions(self) -> List[Position]:
        if any(isinstance(element, Chord) for element in self.notes):
            raise Exception("Cannot extract positions between chords and notes.")
        return [note.position for note in self.notes]

    @property
    def raw_intervals(self) -> List[Optional[int]]:
        if any(isinstance(element, Chord) for element in self.notes):
            raise Exception("Cannot extract intervals between chords and notes.")

        def parse(left_note: Note, right_note: Note) -> Optional[int]:
            if left_note.is_rest() or right_note.is_rest():
                return None
            return (right_note.position - left_note.position).value

        return [parse(self.notes[i - 1], self.notes[i]) for i in range(1, len(self.notes))]

    @property
    def raw_durations(self) -> List[Decimal]:
        if any(isinstance(element, Chord) for element in self.notes):
            raise Exception("Cannot extract durations between chords and notes.")
        return [note.duration.raw_duration for note in self.notes]

    @property
    def raw_rel_positions(self) -> List[int]:
        if any(isinstance(element, Chord) for element in self.notes):
            raise Exception("Cannot extract positions between chords and notes.")
        return [(note.position.rel_position if note.position is not None else None) for note in self.notes]

    @property
    def raw_abs_positions(self) -> List[int]:
        if any(isinstance(element, Chord) for element in self.notes):
            raise Exception("Cannot extract positions between chords and notes.")
        return [(note.position.abs_position if note.position is not None else None) for note in self.notes]

    def append_note(self, note: Note) -> None:
        self.notes.append(note)

    def extend_notes(self, other: NoteSequence) -> None:
        self.notes.extend(other.notes)

    def merge_last_note(self, other: Note) -> None:
        self.notes[-1].extend_duration(other)

    def stack_last_note(self, other: Note) -> None:
        if isinstance(self.notes[-1], Note):
            self.notes[-1] = Chord([self.notes[-1], other])
        elif isinstance(self.notes[-1], Chord):
            self.notes[-1].add_note(other)

    def next_note_idx(self, start: int = 0) -> Optional[int]:
        ref = start + 1
        while ref < len(self.notes):
            if not self.notes[ref].is_rest():
                return ref
            ref += 1
        return None

    def next_rest_idx(self, start: int = 0) -> Optional[int]:
        ref = start + 1
        while ref < len(self.notes):
            if self.notes[ref].is_rest():
                return ref
            ref += 1
        return None

    def lstrip_rests(self) -> None:
        strip_idx = self.next_note_idx(0)
        if not self.notes[0].is_rest() and strip_idx == 1:
            return
        del self.notes[:strip_idx]

    def optimize(self) -> NoteSequence:
        if len(self.notes) <= 0:
            return self
        result: List[Note] = [self.notes[0]]
        for i in range(1, len(self.notes)):
            if self.notes[i].is_rest() and result[-1].is_rest():
                if self.notes[i].is_tagged() == result[-1].is_tagged():
                    result[-1].extend_duration(self.notes[i])
                else:
                    result.append(self.notes[i])
            else:
                result.append(self.notes[i])
        self.notes = result
        return self

    def flatten(self) -> None:
        flattened_notes = list()
        for i in range(len(self.notes)):
            if isinstance((chord := self.notes[i]), Chord):
                flattened_notes.extend(chord.notes)
            else:
                flattened_notes.append(self.notes[i])
        self.notes = flattened_notes
