from dataclasses import dataclass
from typing import Callable


@dataclass
class StrategyContribution:
    strategy_id: str
    strategy: Callable # 类本身
    