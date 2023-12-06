from data.generation.models.annotated_note_sequence import AnnotatedNoteSequence


def non_consecutive_finger_crossing(sequence: AnnotatedNoteSequence, transition: AnnotatedNoteSequence) -> bool:
    return not (
        sequence.fingerings[-2] < sequence.fingerings[-1]
        and transition.fingerings[0] > transition.fingerings[1]
        and sequence.intervals[-1] < 0
        and transition.intervals[0] > 0
    )
