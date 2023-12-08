from data.generation.models.annotated_note_sequence import AnnotatedNoteSequence


class NoteSequenceExtender:
    def __init__(self, ref_sequence: AnnotatedNoteSequence, infer_fingerings: bool = True) -> None:
        self._ref_sequence: AnnotatedNoteSequence = ref_sequence
        self._infer_fingerings: bool = infer_fingerings

    def half_sine(self, scale: int = 1) -> AnnotatedNoteSequence:
        extension: AnnotatedNoteSequence = self._ref_sequence * scale + self._ref_sequence.reverse * scale
        if self._infer_fingerings:
            mid: int = (len(extension) - 1) // 2
            extension.fingerings[mid] = extension.fingerings[mid - 1] + 1
        return extension
