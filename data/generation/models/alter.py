class Alter:
    SYMBOL_MAP = {-2: "bb", -1: "b", 0: "", 1: "#", 2: "x"}

    def __init__(self, value: int) -> None:
        assert -2 <= value <= 2
        self._value = value

    @property
    def symbol(self) -> str:
        return self.SYMBOL_MAP[self._value]

    def increment(self):
        self._value += 1

    def decrement(self):
        self._value -= 1

    @classmethod
    def build(cls, symbol: str):
        assert symbol in cls.SYMBOL_MAP.values()
        return cls({symbol: alter for alter, symbol in cls.SYMBOL_MAP.items()}[symbol])
