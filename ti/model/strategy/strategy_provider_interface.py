from abc import ABC

from ti.model.strategy.strategy_contribution import StrategyContribution


class IStrategyProvider(ABC):
    """
    一个ABC类
    供插件继承使用
    继承这个类代表有strategy可以提供
    """
    
    @property
    def strategy_contribution(self) -> StrategyContribution:
        pass