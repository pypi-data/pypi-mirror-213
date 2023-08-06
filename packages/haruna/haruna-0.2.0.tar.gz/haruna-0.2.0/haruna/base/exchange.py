from .account import Account
from .order import Order


class Exchange:

    def __init__(self, account: Account):
        self.account = account

    def submit_order(self, order: Order):
        pass