import numpy as np
import pandas as pd


def ts(y, start='1990', freq='A'):
    """
    Converts a numpy vector or matrix into a pandas time series
    """
    if isinstance(y, list):
        y = np.array(y)
    elif isinstance(y, pd.Series) or isinstance(y, pd.DataFrame):
        return y
    if len(y.shape) > 1 and y.shape[0] < y.shape[1]:
        y = y.T
    time = pd.date_range(start=start, periods=y.shape[0], freq=freq)
    y = np.array(y, dtype=float)
    if len(y.shape) > 1:
        return pd.DataFrame(y, time)
    else:
        return pd.Series(y, time)


