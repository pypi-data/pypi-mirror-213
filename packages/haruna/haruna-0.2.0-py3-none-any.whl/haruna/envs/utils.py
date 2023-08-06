from typing import Optional

import pandas as pd


def clamp_df(df: pd.DataFrame, start: Optional[str] = None, end: Optional[str] = None):
    if start is not None:
        df = df.loc[start:]
    if end is not None:
        df = df.loc[:end]
    return df
