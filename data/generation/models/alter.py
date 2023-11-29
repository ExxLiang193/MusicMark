class Alter:
    SYMBOL_MAP = {-3: "bbb", -2: "bb", -1: "b", 0: "", 1: "#", 2: "x", 3: "#x"}

    def __init__(self, value: int) -> None:
        assert -3 <= value <= 3
        self._value = value

    @property
    def symbol(self) -> str:
        return self.SYMBOL_MAP[self._value]

    def increment(self, amount: int = 1):
        self._value += amount

    def decrement(self, amount: int = 1):
        self._value -= amount

    @classmethod
    def build(cls, symbol: str):
        assert symbol in cls.SYMBOL_MAP.values()
        return cls({symbol: alter for alter, symbol in cls.SYMBOL_MAP.items()}[symbol])
