from __future__ import annotations
import pandas as pd

__all__ = ["ema20"]

def ema20(close: pd.Series) -> pd.Series:
    """
    Point-in-time EMA(20) using pandas' ewm with adjust=False.
    Input: pd.Series of close prices (index preserved).
    Output: pd.Series of EMA values aligned 1:1 with input.
    """
    s = pd.Series(close, copy=True)
    ema = s.ewm(span=20, adjust=False).mean()
    return ema
