from enum import Enum


class ScaleType(Enum):
    NATURAL = "NATURAL"
    HARMONIC = "HARMONIC"
    MELODIC = "MELODIC"


class ScaleMode(Enum):
    IONIAN = 0
    DORIAN = 1
    PHRYGIAN = 2
    LYDIAN = 3
    MIXOLYDIAN = 4
    AEOLIAN = 5
    LOCRIAN = 6