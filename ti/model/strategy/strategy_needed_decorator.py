import functools
from typing import TypeVar

from ti.model.strategy.strategy_repository import StrategyRepository

P = TypeVar("P", bound=object)

def strategy_needed(protocol: type[P]):
    if not protocol:
        print("[WRAPPER]: must input a protocol")

    def actual_wrapper(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            rep = StrategyRepository.get_instance()
            strategy = rep.get_strategy(protocol) # 不同内存地址
            
            if not strategy:
                strategy = None
                
            return func(*args,**kwargs,strategy = strategy)
        return wrapper
    return actual_wrapper