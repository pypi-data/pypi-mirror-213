import math
from typing import Optional
from typing import Tuple

import gymnasium as gym
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_ta as ta
from cryptodataset.ccxt import CCXTData
from loguru import logger

from .utils import clamp_df

SPREAD_INDEX = 0
SKEW_INDEX = 1


def clamp(x, min_value, max_value):
    return max(min(x, max_value), min_value)


class MarketMakingEnv(gym.Env):

    def __init__(
        self,
        # dataset
        root: str = 'data',
        exchange: str = 'binance',
        symbol: str = 'BTC/USDT',
        timeframe: str = '1m',
        start: Optional[str] = None,
        end: Optional[str] = None,
        download: bool = False,
        # indicators
        atr_window: int = 14,
        rsi_window: int = 14,
        # asccount
        init_quote_balance: float = 25_000,
        init_base_balance: float = 1.0,
        # order
        quantity: float = 0.01,
        # reward
        penalty: float = 0.1,
        spread_factor: float = 4.0,
        skew_factor: float = 0.25,
    ):
        self.root = root
        self.exchange = exchange
        self.symbol = symbol.replace("/", "").upper()
        self.timeframe = timeframe
        self.start = start
        self.end = end
        self.download = download
        self.atr_window = atr_window
        self.rsi_window = rsi_window
        self.init_quote_balance = init_quote_balance
        self.init_base_balance = init_base_balance
        self.quantity = quantity
        self.penalty = penalty
        self.spread_factor = spread_factor
        self.skew_factor = skew_factor

        self.observation_space = self.get_observation_space()
        self.action_space = self.get_action_space()

        self.df = self.load_df()

        self.i_step = None
        self.quote_balance = None
        self.base_balance = None
        self.account_values = None
        self.rewards = None
        self.trading_volume = 0
        self.trading_volumes = None
        self.quote_balances = None
        self.base_balances = None

    def load_df(self) -> pd.DataFrame:
        df = CCXTData(self.exchange).download_ohlcv(self.symbol,
                                                    self.timeframe,
                                                    output_dir=self.root,
                                                    skip=not self.download)

        df['rsi'] = ta.rsi(df['close'], length=self.rsi_window)
        df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=self.atr_window)

        # drop na rows
        df.dropna(inplace=True)

        # set datetime as index
        df.set_index('datetime', inplace=True)

        df = clamp_df(df, self.start, self.end)

        return df

    def get_observation_space(self):
        return gym.spaces.Box(low=-1, high=1, shape=(5,), dtype=np.float64)

    def get_action_space(self):
        return gym.spaces.Box(low=-1, high=1, shape=(2,), dtype=np.float64)

    def _get_obs(self) -> np.ndarray:
        s = self.df.iloc[self.i_step]

        quote_weight = self.quote_balance / self.get_account_value()
        base_weight = self.base_balance * s.close / self.get_account_value()

        assert math.isclose(quote_weight + base_weight,
                            1.0), f'quote_weight: {quote_weight}, base_weight: {base_weight}'

        t = [
            (s.open - s.close) / s.close,
            (s.rsi - 50) / 50,
            s.atr / s.close,
            quote_weight,
            base_weight,
        ]

        return np.array(t, dtype=np.float64)

    def _get_info(self):
        return {}

    def get_mid_price(self) -> float:
        return float(self.df.iloc[self.i_step].close)

    def get_ohlcv(self) -> np.ndarray:
        s = self.df.iloc[self.i_step]

        ohlcv = ['open', 'high', 'low', 'close', 'volume']
        return [float(v) for v in s[ohlcv]]

    def get_price_movement(self) -> float:
        return float(self.df.iloc[self.i_step].close - self.df.iloc[self.i_step - 1].close)

    def get_account_value(self) -> float:
        return self.quote_balance + self.base_balance * self.get_mid_price()

    def get_volatility(self) -> float:
        vol = self.df.iloc[self.i_step].atr / self.df.iloc[self.i_step].close
        return float(vol)

    def buy(self, price, quantity):
        quantity = min(quantity, self.quote_balance / price)
        if self.quote_balance - price * quantity < 0:
            return
        self.quote_balance -= price * quantity
        self.base_balance += quantity

        self.trading_volume += quantity

    def sell(self, price, quantity):
        quantity = min(quantity, self.base_balance)
        if self.base_balance - quantity < 0:
            return
        self.quote_balance += price * quantity
        self.base_balance -= quantity

        self.trading_volume += quantity

    def make_market(self, sell_price, sell_qty, buy_price, buy_qty):
        open_price, high_price, low_price, close_price, volume = self.get_ohlcv()

        if sell_price < high_price and buy_price > low_price:
            # both sides have touched

            total_qty = sell_qty + buy_qty
            if total_qty > volume:
                # volume is not enough
                sell_qty = sell_qty * volume / total_qty
                buy_qty = buy_qty * volume / total_qty

            self.sell(sell_price, sell_qty)
            self.buy(buy_price, buy_qty)

        elif sell_price < high_price and buy_price < low_price:
            # only sell side has touched
            sell_qty = min(sell_qty, volume)
            self.sell(sell_price, sell_qty)

        elif sell_price > high_price and buy_price > low_price:
            # only buy side has touched
            buy_qty = min(buy_qty, volume)
            self.buy(buy_price, buy_qty)

    def reset(self, seed=None, options=None) -> Tuple[np.ndarray, dict]:
        """Reset the environment."""
        super().reset(seed=seed)
        self.i_step = 0

        self.quote_balance = self.init_quote_balance
        self.base_balance = self.init_base_balance

        obs = self._get_obs()

        self.account_values = [self.get_account_value()]
        self.trading_volumes = []
        self.rewards = []
        self.quote_balances = [self.quote_balance]
        self.base_balances = [self.base_balance]

        return obs, {}

    def step(self, action: np.ndarray):
        volatility = self.get_volatility()
        spread_ratio = abs(float(action[SPREAD_INDEX]))
        skew_ratio = abs(float(action[SKEW_INDEX]))

        assert spread_ratio >= 0, f'spread_ratio: {spread_ratio}'
        # assert skew_ratio >= 0, f'skew_ratio: {skew_ratio}'

        mid_price = self.get_mid_price()
        r = self.spread_factor * volatility * spread_ratio / 2.0

        # sell price
        sell_price = mid_price * (1 + r - self.skew_factor * r * skew_ratio)
        # buy price
        buy_price = mid_price * (1 - r - self.skew_factor * r * skew_ratio)

        assert sell_price >= buy_price

        sell_qty = min(self.quantity, self.base_balance)
        buy_qty = min(self.quantity, self.quote_balance / buy_price)

        prev_value = self.get_account_value()

        self.i_step += 1

        self.trading_volume = 0

        if sell_price != buy_price and sell_price > mid_price and buy_price < mid_price:
            assert sell_price != mid_price
            assert buy_price != mid_price
            self.make_market(sell_price, sell_qty, buy_price, buy_qty)

        self.trading_volumes += [self.trading_volume]

        obs = self._get_obs()
        info = self._get_info()

        self.account_values.append(self.get_account_value())
        self.quote_balances.append(self.quote_balance)
        self.base_balances.append(self.base_balance)

        # calculate reward
        pnl = self.get_account_value() - prev_value
        reward = pnl - self.penalty * max(self.base_balance - self.init_base_balance, 0) * self.get_price_movement()
        self.rewards += [reward]

        terminated = self.i_step >= len(self.df) - 1

        if self.quote_balance < 0:
            logger.warning('#{} quote balance: {} is negative'.format(self.i_step, self.quote_balance))
            self.quote_balance = max(self.quote_balance, 0)

        if self.base_balance < 0:
            logger.warning('#{} base balance: {} is negative'.format(self.i_step, self.base_balance))
            self.base_balance = max(self.base_balance, 0)

        return obs, reward, terminated, 0, info

    def render(self):
        pass

    def close(self):
        pass

    def plot(self):
        fig, ax = plt.subplots(3, 2, figsize=(16, 9))

        ax[0, 0].set_title('Account Value')
        ax[0, 0].plot(self.account_values)

        ax[1, 0].set_title('Close Price')
        ax[1, 0].plot(self.df['close'])

        ax[2, 0].set_title('Accumulated Reward')
        ax[2, 0].plot(np.array(self.rewards).cumsum())

        ax[0, 1].set_title('Accumulated Trading Volume')
        ax[0, 1].plot(np.array(self.trading_volumes).cumsum())

        ax[1, 1].set_title('Quote Balance')
        ax[1, 1].plot(self.quote_balances)

        ax[2, 1].set_title('Base Balance')
        ax[2, 1].plot(self.base_balances)

        plt.plot()
