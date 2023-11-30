from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from data.generation.models.interval import Interval


@dataclass(frozen=True)
class ScaleIntervals:
    MAJOR: Tuple[Interval, ...] = tuple(Interval(value) for value in (2, 2, 1, 2, 2, 2, 1))
    MINOR_NATURAL: Tuple[Interval, ...] = tuple(Interval(value) for value in (2, 1, 2, 2, 1, 2, 2))
    MINOR_HARMONIC: Tuple[Interval, ...] = tuple(Interval(value) for value in (2, 1, 2, 2, 1, 3, 1))
    MINOR_MELODIC: Tuple[Interval, ...] = tuple(Interval(value) for value in (2, 1, 2, 2, 2, 2, 1))


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
