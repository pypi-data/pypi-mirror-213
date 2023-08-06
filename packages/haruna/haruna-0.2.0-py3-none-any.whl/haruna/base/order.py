from .enum import Side


class Order:

    def __init__(self, symbol: str, side: Side, quantity: float):
        self.symbol = symbol
        self.side = side
        self.quantity = quantity