from data.generation.builders.note_sequence_extender import NoteSequenceExtender
from data.generation.models.annotated_note_sequence import AnnotatedNoteSequence
from data.generation.models.arpeggio import Arpeggio
from data.generation.models.arpeggio_fingerings import ArpeggioFingerings
from data.generation.models.chords import SEVENTH_CHORD_CLASSES, TRIAD_CHORD_CLASSES
from data.generation.models.constants import Inversion, ScaleMode, ScaleType
from data.generation.models.interval import Interval
from data.generation.models.major_scale import MajorScale
from data.generation.models.minor_scale import MinorScale
from data.generation.models.note import Note
from data.generation.models.scale_fingerings import ScaleFingerings

BASE_NOTES = ("C#", "F#", "B", "E", "A", "D", "G", "C", "F", "Bb", "Eb", "Ab", "Db", "Gb", "Cb")


def generate_sequences():
    for base_note_name in BASE_NOTES:
        for scale_mode in ScaleMode:
            scale = MajorScale.build(base_note_name, scale_mode)
            fingerings = ScaleFingerings.build(scale)
            annotations = AnnotatedNoteSequence(scale.notes, fingerings.values, scale.intervals)
            extender = NoteSequenceExtender(annotations)
            yield extender.half_sine(2)

    for base_note_name in BASE_NOTES:
        for scale_mode in ScaleMode:
            scale = MinorScale.build(base_note_name, ScaleType.NATURAL, scale_mode)
            fingerings = ScaleFingerings.build(scale)
            annotations = AnnotatedNoteSequence(scale.notes, fingerings.values, scale.intervals)
            extender = NoteSequenceExtender(annotations)
            yield extender.half_sine(2)

    for base_note_name in BASE_NOTES:
        for scale_mode in ScaleMode:
            scale = MinorScale.build(base_note_name, ScaleType.HARMONIC, scale_mode)
            fingerings = ScaleFingerings.build(scale)
            annotations = AnnotatedNoteSequence(scale.notes, fingerings.values, scale.intervals)
            extender = NoteSequenceExtender(annotations)
            yield extender.half_sine(2)

    for base_note_name in BASE_NOTES:
        for scale_mode in ScaleMode:
            scale = MinorScale.build(base_note_name, ScaleType.MELODIC, scale_mode)
            fingerings = ScaleFingerings.build(scale)
            annotations = AnnotatedNoteSequence(scale.notes, fingerings.values, scale.intervals)
            extender = NoteSequenceExtender(annotations)
            yield extender.half_sine(2)

    for base_note_name in BASE_NOTES:
        for inversion in (Inversion.ROOT, Inversion.TRIAD_FIRST, Inversion.TRIAD_SECOND):
            for chord_class in TRIAD_CHORD_CLASSES:
                arpeggio = Arpeggio.build(base_note_name, chord_class, inversion)
                fingerings = ArpeggioFingerings.build(arpeggio)
                annotations = AnnotatedNoteSequence(arpeggio.notes, fingerings.values, arpeggio.intervals)
                extender = NoteSequenceExtender(annotations)
                yield extender.half_sine(2)

    for base_note_name in BASE_NOTES:
        for inversion in (Inversion.ROOT, Inversion.SEVENTH_FIRST, Inversion.SEVENTH_SECOND, Inversion.SEVENTH_THIRD):
            for chord_class in SEVENTH_CHORD_CLASSES:
                arpeggio = Arpeggio.build(base_note_name, chord_class, inversion)
                fingerings = ArpeggioFingerings.build(arpeggio)
                annotations = AnnotatedNoteSequence(arpeggio.notes, fingerings.values, arpeggio.intervals)
                extender = NoteSequenceExtender(annotations)
                yield extender.half_sine(2)

    for base_note_name in BASE_NOTES:
        annotations = AnnotatedNoteSequence(
            notes=[Note.build_from_name(base_note_name), Note.build_from_name(base_note_name)],
            fingerings=[1, 5],
            intervals=(Interval(12),),
            infer_fingerings=False,
        )
        extender = NoteSequenceExtender(annotations)
        yield extender.half_sine(1)
