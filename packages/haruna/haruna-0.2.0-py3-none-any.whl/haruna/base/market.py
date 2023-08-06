SYMBOL_TO_BASE_QUOTE = {
    'BTCUSDT': ('BTC', 'USDT'),
    'ETHUSDT': ('ETH', 'USDT'),
    'BNBUSDT': ('BNB', 'USDT'),
    'ADAUSDT': ('ADA', 'USDT'),
    'XRPUSDT': ('XRP', 'USDT'),
    'DOTUSDT': ('DOT', 'USDT'),
    'LTCUSDT': ('LTC', 'USDT'),
    'LINKUSDT': ('LINK', 'USDT'),
    'BCHUSDT': ('BCH', 'USDT'),
}


class Market:

    def __init__(self, symbol: str):
        self.symbol = symbol
        self.base_currency, self.quote_currency = SYMBOL_TO_BASE_QUOTE[symbol]
