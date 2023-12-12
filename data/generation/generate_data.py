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
from typing import Dict, Final, Iterable, List, Tuple

# Removed Cb because it's enharmonic to B
BASE_NOTES = ("C#", "F#", "B", "E", "A", "D", "G", "C", "F", "Bb", "Eb", "Ab", "Db", "Gb")

FingerIntervals = namedtuple("FingerInterval", ("from_finger", "to_finger", "intervals"))
_SPECIAL_INTERVALS: Dict[Tuple[int, int], Iterable] = {
    (1, 3): range(-2, 13),  # -2 to 12 inclusive
    (1, 4): range(0, 15),  # 0 to 14 inclusive
    (1, 5): range(3, 17),  # 3 to 16 inclusive
    (2, 5): range(3, 11),  # 3 to 10 inclusive
    (3, 5): range(3, 8),  # 3 to 9 inclusive
}
FINGERS_INTERVALS: Final[List[FingerIntervals]] = [
    FingerIntervals(from_finger=i, to_finger=j, intervals=_SPECIAL_INTERVALS[(i, j)])
    if (i, j) in _SPECIAL_INTERVALS
    else FingerIntervals(from_finger=i, to_finger=j, intervals=range(0, 1))
    for i in range(1, 6)
    for j in range(1, 6)
]


def generate_sequences(rh: bool = True):
    for base_note_name in BASE_NOTES:
        for scale_mode in ScaleMode:
            scale = MajorScale.build(base_note_name, scale_mode, rh)
            fingerings = ScaleFingerings.build(scale)
            annotations = AnnotatedNoteSequence(scale.notes, fingerings.values, scale.intervals)
            extender = NoteSequenceExtender(annotations)
            yield extender.half_sine(1)

    for base_note_name in BASE_NOTES:
        for scale_mode in ScaleMode:
            scale = MinorScale.build(base_note_name, ScaleType.NATURAL, scale_mode, rh)
            fingerings = ScaleFingerings.build(scale)
            annotations = AnnotatedNoteSequence(scale.notes, fingerings.values, scale.intervals)
            extender = NoteSequenceExtender(annotations)
            yield extender.half_sine(1)

    for base_note_name in BASE_NOTES:
        for scale_mode in ScaleMode:
            scale = MinorScale.build(base_note_name, ScaleType.HARMONIC, scale_mode, rh)
            fingerings = ScaleFingerings.build(scale)
            annotations = AnnotatedNoteSequence(scale.notes, fingerings.values, scale.intervals)
            extender = NoteSequenceExtender(annotations)
            yield extender.half_sine(1)

    for base_note_name in BASE_NOTES:
        for scale_mode in ScaleMode:
            scale = MinorScale.build(base_note_name, ScaleType.MELODIC, scale_mode, rh)
            fingerings = ScaleFingerings.build(scale)
            annotations = AnnotatedNoteSequence(scale.notes, fingerings.values, scale.intervals)
            extender = NoteSequenceExtender(annotations)
            yield extender.half_sine(1)

    for base_note_name in BASE_NOTES:
        for inversion in (Inversion.ROOT, Inversion.TRIAD_FIRST, Inversion.TRIAD_SECOND):
            for chord_class in TRIAD_CHORD_CLASSES:
                arpeggio = Arpeggio.build(base_note_name, chord_class, inversion, rh)
                fingerings = ArpeggioFingerings.build(arpeggio)
                annotations = AnnotatedNoteSequence(arpeggio.notes, fingerings.values, arpeggio.intervals)
                extender = NoteSequenceExtender(annotations)
                yield extender.half_sine(2)

    for base_note_name in BASE_NOTES:
        for inversion in (Inversion.ROOT, Inversion.SEVENTH_FIRST, Inversion.SEVENTH_SECOND, Inversion.SEVENTH_THIRD):
            for chord_class in SEVENTH_CHORD_CLASSES:
                arpeggio = Arpeggio.build(base_note_name, chord_class, inversion, rh)
                fingerings = ArpeggioFingerings.build(arpeggio)
                annotations = AnnotatedNoteSequence(arpeggio.notes, fingerings.values, arpeggio.intervals)
                extender = NoteSequenceExtender(annotations)
                yield extender.half_sine(2)

    for base_note_name in BASE_NOTES:
        for finger_intervals in FINGERS_INTERVALS:
            for interval in finger_intervals.intervals:
                interval = Interval(interval if rh else -interval)
                annotations = AnnotatedNoteSequence(
                    notes=[
                        Note.build_from_name(base_note_name),
                        Note.build_from_name(base_note_name) + interval,
                    ],
                    fingerings=[finger_intervals.from_finger, finger_intervals.to_finger],
                    intervals=(interval,),
                )
                extender = NoteSequenceExtender(annotations, infer_fingerings=False)
                yield extender.half_sine(1)
