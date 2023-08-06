from typing import List

from .balance import Balance


class Account:

    def __init__(self, balances: List[Balance]):
        self.balances = balances
