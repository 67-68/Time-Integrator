from dataclasses import dataclass


@dataclass
class FunctionContribution:
    """
    用来登记插件的函数
    """
    func: callable
    func_id: str