from collections import defaultdict, deque
from typing import Dict, Generator, List, Set, Tuple

from data.generation.builders.note_sequence_filters import non_consecutive_finger_crossing
from data.generation.models.annotated_note_sequence import AnnotatedNoteSequence


class NoteSequencePermuter:
    def __init__(self, sequence_source: Generator[AnnotatedNoteSequence, None, None], stride: int = 1) -> None:
        assert stride >= 1
        self._prefix_map: Dict[Tuple[int, int], Set[AnnotatedNoteSequence]] = self._compute_map(sequence_source, stride)
        self._transition_filters = (non_consecutive_finger_crossing,)

    def _compute_map(
        self,
        sequence_source: Generator[AnnotatedNoteSequence, None, None],
        stride: int,
    ) -> Dict[Tuple[int, int], Set[AnnotatedNoteSequence]]:
        prefix_map: Dict[Tuple[int, int], Set[AnnotatedNoteSequence]] = defaultdict(set)
        for sequence in sequence_source:
            for i in range(len(sequence) - stride):
                prefix_map[(sequence.notes[i], sequence.fingerings[i])].add(sequence[i : i + 1 + stride])
        return prefix_map

    def permute(self, length: int) -> List[AnnotatedNoteSequence]:
        queue = deque(pair for pairs in self._prefix_map.values() for pair in pairs)
        results: List[AnnotatedNoteSequence] = list()
        while queue:
            sequence: AnnotatedNoteSequence = queue.popleft()
            if len(sequence) >= length:
                results.append(sequence)
                continue
            for transition in self._prefix_map[(sequence.notes[-1], sequence.fingerings[-1])]:
                if all(transition_filter(sequence, transition) for transition_filter in self._transition_filters):
                    queue.append(sequence + transition)
        return results
