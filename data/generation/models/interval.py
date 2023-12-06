from __future__ import annotations


class Interval:
    def __init__(self, value: int) -> None:
        self.value: int = value

    def __repr__(self) -> str:
        return str(self.value)

    def __add__(self, other: Interval | int) -> Interval | int:
        if isinstance(other, int):
            return Interval(self.value + other)
        elif isinstance(other, Interval):
            return Interval(self.value + other.value)

    def __radd__(self, other: Interval | int) -> Interval | int:
        if isinstance(other, int):
            return self.value + other
        elif isinstance(other, Interval):
            return Interval(self.value + other.value)

    def __sub__(self, other: Interval | int) -> Interval | int:
        if isinstance(other, int):
            return self.value - other
        elif isinstance(other, Interval):
            return Interval(self.value - other.value)

    def __mod__(self, other: int) -> Interval:
        return Interval(self.value % other)

    def __eq__(self, other: Interval) -> bool:
        return self.value == other.value

    def __lt__(self, other: Interval | int) -> bool:
        if isinstance(other, int):
            return self.value < other
        elif isinstance(other, Interval):
            return self.value < other.value

    def __gt__(self, other: Interval | int) -> bool:
        if isinstance(other, int):
            return self.value > other
        elif isinstance(other, Interval):
            return self.value > other.value

    @property
    def inverse(self):
        return Interval(-self.value)
