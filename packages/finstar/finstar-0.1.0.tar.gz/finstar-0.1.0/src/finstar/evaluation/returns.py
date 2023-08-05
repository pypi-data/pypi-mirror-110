import numpy as np
import pandas as pd


def log_returns(series: pd.Series) -> pd.Series:
    return np.log(series / series.shift(1))


def strategy_returns(positions: pd.Series, returns: pd.Series) -> pd.Series:
    return positions.shift(1) * returns
