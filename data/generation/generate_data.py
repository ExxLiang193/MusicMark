from data.generation.models.arpeggio import Arpeggio
from data.generation.models.arpeggio_fingerings import ArpeggioFingerings
from data.generation.models.chords import (AUG5Chord, AUGMAJ7Chord, DIM5Chord,
                                           DIM7Chord, DOM7Chord, HalfDIM7Chord,
                                           MAJ5Chord, MAJ7Chord, MIN5Chord,
                                           MIN7Chord, MINMAJ7Chord)
from data.generation.models.constants import Inversion, ScaleType
from data.generation.models.major_scale import MajorScale
from data.generation.models.minor_scale import MinorScale
from data.generation.models.scale_fingerings import ScaleFingerings

BASE_NOTES = (
    ("C#", "#" * 7),
    ("F#", "#" * 6),
    ("B", "#" * 5),
    ("E", "#" * 4),
    ("A", "#" * 3),
    ("D", "#" * 2),
    ("G", "#" * 1),
    ("C", ""),
    ("F", "b" * 1),
    ("Bb", "b" * 2),
    ("Eb", "b" * 3),
    ("Ab", "b" * 4),
    ("Db", "b" * 5),
    ("Gb", "b" * 6),
    ("Cb", "b" * 7),
)
TRIAD_CHORD_CLASSES = (
    MAJ5Chord,
    MIN5Chord,
    DIM5Chord,
    AUG5Chord,
)
SEVENTH_CHORD_CLASSES = (
    MAJ7Chord,
    MIN7Chord,
    DOM7Chord,
    DIM7Chord,
    HalfDIM7Chord,
    MINMAJ7Chord,
    AUGMAJ7Chord,
)

print("-" * 10, "MAJOR SCALES", "-" * 10)
for base_note_name, accidentals in BASE_NOTES:
    print((scale := MajorScale.build(base_note_name)), ScaleFingerings.build(scale), accidentals)

print("-" * 10, "MINOR (NATURAL) SCALES", "-" * 10)
for base_note_name, accidentals in BASE_NOTES:
    print((scale := MinorScale.build(base_note_name)), ScaleFingerings.build(scale), accidentals)

print("-" * 10, "MINOR (HARMONIC) SCALES", "-" * 10)
for base_note_name, accidentals in BASE_NOTES:
    print((scale := MinorScale.build(base_note_name, ScaleType.HARMONIC)), ScaleFingerings.build(scale), accidentals)

print("-" * 10, "MINOR (MELODIC) SCALES", "-" * 10)
for base_note_name, accidentals in BASE_NOTES:
    print((scale := MinorScale.build(base_note_name, ScaleType.MELODIC)), ScaleFingerings.build(scale), accidentals)

print("-" * 10, "TRIAD CHORD ARPEGGIOS", "-" * 10)
for base_note_name, _ in BASE_NOTES:
    for inversion in (Inversion.ROOT, Inversion.TRIAD_FIRST, Inversion.TRIAD_SECOND):
        print("-" * 5, inversion.name, "-" * 5)
        for chord_class in TRIAD_CHORD_CLASSES:
            class_name = chord_class.__name__
            print(
                (arpeggio := Arpeggio.build(base_note_name, chord_class, inversion)),
                ArpeggioFingerings.build(arpeggio),
                class_name,
            )

print("-" * 10, "SEVENTH CHORD ARPEGGIOS", "-" * 10)
for base_note_name, _ in BASE_NOTES:
    for inversion in (Inversion.ROOT, Inversion.TRIAD_FIRST, Inversion.TRIAD_SECOND):
        print("-" * 5, inversion.name, "-" * 5)
        for chord_class in SEVENTH_CHORD_CLASSES:
            class_name = chord_class.__name__
            print(
                (arpeggio := Arpeggio.build(base_note_name, chord_class, inversion)),
                ArpeggioFingerings.build(arpeggio),
                class_name,
            )
