class NoteName:
    WHITE_POSITIONS = (0, 2, 4, 5, 7, 9, 11)
    BLACK_POSITIONS = (1, 3, 6, 8, 10)
    NAME_MAP = {0: "C", 1: "D", 2: "E", 3: "F", 4: "G", 5: "A", 6: "B"}

    def __init__(self, name_position: int) -> None:
        assert name_position in self.WHITE_POSITIONS
        self.name_position: int = name_position

    @property
    def name(self) -> str:
        return self.NAME_MAP[self.WHITE_POSITIONS.index(self.name_position)]

    def increment(self, in_place=False):
        new_rel_position = self.WHITE_POSITIONS[
            (self.WHITE_POSITIONS.index(self.name_position) + 1) % len(self.WHITE_POSITIONS)
        ]
        if in_place:
            self.name_position = new_rel_position
        else:
            return NoteName(new_rel_position)

    def decrement(self, in_place=False):
        new_rel_position = self.WHITE_POSITIONS[
            (self.WHITE_POSITIONS.index(self.name_position) - 1) % len(self.WHITE_POSITIONS)
        ]
        if in_place:
            self.name_position = new_rel_position
        else:
            return NoteName(new_rel_position)

    @classmethod
    def build(cls, name: str):
        assert name in cls.NAME_MAP.values()
        return cls(cls.WHITE_POSITIONS[{note_name: position for position, note_name in cls.NAME_MAP.items()}[name]])
