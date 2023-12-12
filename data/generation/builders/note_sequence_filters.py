from data.generation.models.annotated_note_sequence import AnnotatedNoteSequence


def non_consecutive_finger_crossing(
    sequence: AnnotatedNoteSequence,
    transition: AnnotatedNoteSequence,
    rh: bool,
) -> bool:
    return not (
        sequence.fingerings[-2] < sequence.fingerings[-1]
        and transition.fingerings[0] > transition.fingerings[1]
        and ((sequence.intervals[-1] < 0) if rh else (sequence.intervals[-1] > 0))
        and ((transition.intervals[0] > 0) if rh else (transition.intervals[0] < 0))
    )


def non_adjacent_weak_finger_crossing(
    sequence: AnnotatedNoteSequence,
    transition: AnnotatedNoteSequence,
    rh: bool,
) -> bool:
    if sequence.fingerings[-1] == 1 or transition.fingerings[1] == 1:
        return True
    test: int = (transition.fingerings[1] - transition.fingerings[0]) * transition.intervals[0].value
    return (test >= 0) if rh else (test <= 0)
