import itertools
from typing import Iterable

from data.generation.models.annotated_note_sequence import AnnotatedNoteSequence


class NoteSequenceWriter:
    def __init__(self, note_sequences: Iterable[AnnotatedNoteSequence]) -> None:
        self._note_sequences: Iterable[AnnotatedNoteSequence] = note_sequences

    def to_dsv(self, file_target: str, delimiter: str = " ") -> None:
        with open(file_target, "w+") as f:
            for sequence in self._note_sequences:
                encoded_sequence = delimiter.join(
                    itertools.chain(
                        (f"{len(sequence)}",),
                        (str(note.rel_position) for note in sequence.notes),
                        (str(interval.value) for interval in sequence.intervals),
                        (str(fingering) for fingering in sequence.fingerings),
                    )
                )
                f.write(encoded_sequence + "\n")
