from data.generation.models.annotated_note_sequence import AnnotatedNoteSequence


class NoteSequenceExtender:
    def __init__(self, ref_sequence: AnnotatedNoteSequence) -> None:
        self._ref_sequence: AnnotatedNoteSequence = ref_sequence

    def half_sine(self, scale: int = 1) -> AnnotatedNoteSequence:
        return self._ref_sequence * scale + self._ref_sequence.reverse * scale
