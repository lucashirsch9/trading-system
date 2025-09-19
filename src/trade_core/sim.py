from typing import Any, Dict, List, Tuple

class Strategy:
    def on_bar(self, bar: Dict[str, float]) - ...
    def on_start(self): ...
    def on_end(self): ...

def simulate(strategy: Strategy, bars: list[dict], config: Dict[str, Any]) -, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Return (trades, equity_curve, logs). Stub for now.""" 
    strategy.on_start()
    for bar in bars:
        strategy.on_bar(bar)
    strategy.on_end()
    return [], [], [{"msg": "sim stub ok"}]
