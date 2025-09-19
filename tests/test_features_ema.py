import pandas as pd
import numpy as np

from importlib import import_module

def test_ema20_exists_and_is_pti():
    # import lazily so test fails clearly if module missing
    features = import_module("trade_core.features")

    close = pd.Series([1, 2, 3, 4, 5], dtype=float)
    ema = features.ema20(close)

    # shape & alignment
    assert isinstance(ema, pd.Series)
    assert ema.index.equals(close.index)

    # point-in-time: first value should be finite but not require future bars
    assert np.isfinite(ema.iloc[0])

    # increasing close ⇒ ema should be strictly increasing after first elem
    assert (ema.diff().iloc[1:] > 0).all()

def test_ema_matches_pandas_ewm():
    features = import_module("trade_core.features")
    close = pd.Series([10, 11, 12, 13, 14, 15], dtype=float)

    ours = features.ema20(close)
    ref = close.ewm(span=20, adjust=False).mean()

    pd.testing.assert_series_equal(ours, ref, check_names=False, check_dtype=False)
