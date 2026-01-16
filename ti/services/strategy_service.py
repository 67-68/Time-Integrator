from typing import Callable
from ti.model.strategy.strategy_needed_decorator import strategy_needed
from ti.model.strategy.strategy_repository import StrategyRepository


class StrategyService:
    """
    这个类提供Strategy相关的服务
    无状态
    """
    @staticmethod
    def execute_with_strategy(
        protocol,
        default_function: Callable,
        *args,
        **kwargs
    ):
        """
        立即使用策略（如果可用）或默认函数来执行一个操作。
        接受一个函数，自动获取对应的Strategy作为依赖送入
        """
        # 装饰器在这里用起来有点绕，可以直接调用 Repository
        rep = StrategyRepository.get_instance()
        strategy = rep.get_strategy(protocol)
        
        if strategy:
            method = StrategyService._invoke_method_from_protocol(strategy, protocol)
            return method(*args, **kwargs)
        else:
            return default_function(*args, **kwargs)

    @staticmethod
    def get_strategy_methods_from_protocol(protocol):
        """
        通过Protocol查询所有符合的Strategy
        并获取所有对应的函数
        """
        funcs = []
        rep = StrategyRepository.get_instance()
        strategies = rep.get_all_strategy_from_protocol(protocol)
        for strategy in strategies:
            func = StrategyService._invoke_method_from_protocol(strategy,protocol)
            funcs.append(func)
        
        if not funcs:
            print(f"No Strategy Support this protocol: {protocol}")    
        
        return funcs

    @staticmethod
    def execute_strategies_from_protocol(
        protocol,
    ):
        """
        接受一个protocol
        获取所有对应的Strategy, 执行并返回结果列表

        Args:
            protocol (_type_): _description_
            default_function (Callable): _description_

        Returns:
            _type_: _description_
        """
        strategies_method = StrategyService.get_strategy_methods_from_protocol(protocol)
        
        results = []
        if strategies_method: 
            for strategy_method in strategies_method:
                results.append(strategy_method())
                
        return results

    @staticmethod
    def _invoke_method_from_protocol(
        strategy,
        protocol
    ) -> Callable:
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
        
        