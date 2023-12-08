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
from collections import namedtuple
from typing import Final, List

# Removed Cb because it's enharmonic to B
BASE_NOTES = ("C#", "F#", "B", "E", "A", "D", "G", "C", "F", "Bb", "Eb", "Ab", "Db", "Gb")

FingerIntervals = namedtuple("FingerInterval", ("from_finger", "to_finger", "intervals"))
FINGERS_INTERVALS: Final[List[FingerIntervals]] = [
    FingerIntervals(from_finger=1, to_finger=2, intervals=range(0, 1)),  # 0 only
    FingerIntervals(from_finger=1, to_finger=3, intervals=range(-2, 13)),  # -2 to 12 inclusive
    FingerIntervals(from_finger=1, to_finger=4, intervals=range(0, 15)),  # 0 to 14 inclusive
    FingerIntervals(from_finger=1, to_finger=5, intervals=range(1, 17)),  # 1 to 16 inclusive
    FingerIntervals(from_finger=2, to_finger=3, intervals=range(0, 1)),  # 0 only
    FingerIntervals(from_finger=2, to_finger=5, intervals=range(3, 11)),  # 3 to 10 inclusive
    FingerIntervals(from_finger=3, to_finger=4, intervals=range(0, 1)),  # 0 only
]


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
        for finger_intervals in FINGERS_INTERVALS:
            for interval in finger_intervals.intervals:
                annotations = AnnotatedNoteSequence(
                    notes=[
                        Note.build_from_name(base_note_name),
                        Note.build_from_name(base_note_name) + Interval(interval),
                    ],
                    fingerings=[finger_intervals.from_finger, finger_intervals.to_finger],
                    intervals=(Interval(interval),),
                )
                extender = NoteSequenceExtender(annotations, infer_fingerings=False)
                yield extender.half_sine(1)
