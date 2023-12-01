from collections import defaultdict
from typing import Dict, Generator, Set, Tuple

from data.generation.models.annotated_note_sequence import AnnotatedNoteSequence


class NoteSequencePermuter:
    def __init__(self, sequence_source: Generator[AnnotatedNoteSequence, None, None]) -> None:
        self._prefix_map: Dict[Tuple[int, int], Set[AnnotatedNoteSequence]] = self._compute_map(sequence_source)

    def _compute_map(
        self, sequence_source: Generator[AnnotatedNoteSequence, None, None]
    ) -> Dict[Tuple[int, int], Set[AnnotatedNoteSequence]]:
        result: Dict[Tuple[int, int], Set[AnnotatedNoteSequence]] = defaultdict(set)
        for sequence in sequence_source:
            for i in range(len(sequence) - 1):
                result[(sequence.notes[i], sequence.fingerings[i])].add(sequence[i : i + 2])
        return result

    def permute(self, length: int):
        pass
