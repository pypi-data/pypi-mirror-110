import numpy as np
import pandas as pd


def sma(series: pd.Series, short_period: int, long_period: int) -> pd.Series:
    short_series = series.rolling(short_period).mean()
    long_series = series.rolling(long_period).mean()
    sma_positions = pd.Series(np.where(short_series > long_series, 1, -1))
    # set nan values manually as > above concerts them to bool
    nans = np.isnan(short_series) | np.isnan(long_series)
    sma_positions[nans] = np.nan
    return sma_positions
