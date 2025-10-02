from typing import Callable
from ti.model.strategy.strategy_needed_decorator import strategy_needed


class StrategyService:
    """
    这个类提供Strategy相关的服务
    无状态
    """
    @staticmethod
    def execute_through_strategy(protocol,default_function: Callable):
        @strategy_needed(protocol)
        def actual_function(strategy = None):
            if strategy:
                method = StrategyService._invoke_method_from_protocol(strategy,protocol)
                data = method()
                #TODO: 注意！策略本身可以创建一个Presenter, 但是Presetner需要返回View
            else:
                data = default_function()
        
            return data
        return actual_function()

    @staticmethod
    def _invoke_method_from_protocol(strategy,protocol) -> Callable:
        """
        动态查找 strategy 实例中符合 protocol 的方法。
        约定：protocol 中只应包含一个公开的 (非下划线开头) 方法。
        """
        method_name = None
        # 获取protocol方法
        for attr in dir(protocol):
            if not attr.startswith("_"):
                method_name = attr
        
        if not method_name:
            raise AttributeError(f"Protocol {protocol.__name__} 中没有找到任何公开方法")
        
        if not hasattr(strategy,method_name):
            raise NotImplementedError(f'strategy {strategy.__name__} 中没有实现 protocol {protocol.__name__} 的 {method_name} 方法')
        
        actual_method = getattr(strategy,method_name)
        
        return actual_method
        
        