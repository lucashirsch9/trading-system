from trade_core.sim import simulate, Strategy

class Dummy(Strategy):
    def on_start(self):
        self.seen = 0

    def on_bar(self, bar):
        self.seen += 1

    def on_end(self):
        pass

def test_sim_contract():
    trades, eq, logs = simulate(
        Dummy(),
        [{"open": 1, "high": 1, "low": 1, "close": 1, "volume": 0}],
        {},
    )
    assert isinstance(trades, list)
    assert isinstance(eq, list)
    assert isinstance(logs, list)
