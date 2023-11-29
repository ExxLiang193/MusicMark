from enum import Enum
from dataclasses import dataclass


@dataclass(frozen=True)
class ScaleIntervals:
    MAJOR = (2, 2, 1, 2, 2, 2, 1)
    MINOR_NATURAL = (2, 1, 2, 2, 1, 2, 2)
    MINOR_HARMONIC = (2, 1, 2, 2, 1, 3, 1)
    MINOR_MELODIC = (2, 1, 2, 2, 2, 2, 1)


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


class Inversion(Enum):
    ROOT = 0

    TRIAD_FIRST = 1
    TRIAD_SECOND = 2

    SEVENTH_FIRST = 1
    SEVENTH_SECOND = 2
    SEVENTH_THIRD = 3
