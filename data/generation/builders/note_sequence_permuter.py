import random
from collections import Counter, defaultdict, deque
from typing import Dict, Generator, List, Tuple

from data.generation.builders.note_sequence_filters import (
    non_adjacent_weak_finger_crossing,
    non_consecutive_finger_crossing,
)
from data.generation.models.annotated_note_sequence import AnnotatedNoteSequence


class NoteSequencePermuter:
    def __init__(self, sequence_source: Generator[AnnotatedNoteSequence, None, None], stride: int = 1) -> None:
        assert stride >= 1
        self._prefix_map: Dict[Tuple[int, int], Dict[AnnotatedNoteSequence, int]] = self._compute_map(
            sequence_source, stride
        )
        self._transition_filters = (non_consecutive_finger_crossing, non_adjacent_weak_finger_crossing)

    def _compute_map(
        self,
        sequence_source: Generator[AnnotatedNoteSequence, None, None],
        stride: int,
    ) -> Dict[Tuple[int, int], Dict[AnnotatedNoteSequence, int]]:
        prefix_map = defaultdict(Counter)
        for sequence in sequence_source:
            for i in range(len(sequence) - stride):
                prefix_map[(sequence.notes[i], sequence.fingerings[i])][sequence[i : i + 1 + stride]] += 1
        for key in prefix_map:
            prefix_map[key] = list(prefix_map[key].items())
        return prefix_map

    def permute(self, length: int) -> List[AnnotatedNoteSequence]:
        queue = deque(pair[0] for pairs in self._prefix_map.values() for pair in pairs)
        results: List[AnnotatedNoteSequence] = list()
        while queue:
            sequence: AnnotatedNoteSequence = queue.popleft()
            if len(sequence) >= length:
                results.append(sequence)
                continue
            for transition, _ in self._prefix_map[(sequence.notes[-1], sequence.fingerings[-1])]:
                if all(transition_filter(sequence, transition) for transition_filter in self._transition_filters):
                    queue.append(sequence + transition)
        return results

    def permute_random(self, length: int, amount: int) -> List[AnnotatedNoteSequence]:
        transitions, weights = list(zip(*sum(self._prefix_map.values(), list())))
        queue = deque(random.choices(transitions, weights=weights, k=amount))
        results: List[AnnotatedNoteSequence] = list()
        while queue:
            sequence: AnnotatedNoteSequence = queue.popleft()
            if len(sequence) >= length:
                results.append(sequence)
                continue
            map_choices = self._prefix_map[(sequence.notes[-1], sequence.fingerings[-1])]
            transitions, weights = list(zip(*map_choices))
            transition = random.choices(transitions, weights=weights, k=1)[0]
            if all(transition_filter(sequence, transition) for transition_filter in self._transition_filters):
                queue.append(sequence + transition)
        return results
