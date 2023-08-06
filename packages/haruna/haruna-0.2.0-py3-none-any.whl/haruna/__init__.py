from gymnasium import make
from gymnasium.envs.registration import register

from . import envs
from . import optim
from . import transforms
from . import utils

register(
    id='haruna/TradingEnv-v0',
    entry_point='haruna.envs:TradingEnv',
)

register(
    id='haruna/MarketMaking-v0',
    entry_point='haruna.envs:MarketMaking',
)
