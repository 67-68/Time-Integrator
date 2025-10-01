from abc import ABC,abstractmethod

from ti.model.action_unit import ActionUnit


class ITranslator(ABC):
    """
    在我的设想中，这个类作为所有翻译器类的接口
    任何翻译器类都应该实现
    1. 从actionUnit数据模型类到特殊语法的翻译
    2. 从特殊语法到actionUnit的翻译
    
    鉴于目前翻译需求不大，就不把特殊语言单独作为数据模型列出来了
    翻译器自己包含了就行
    """
    @abstractmethod
    def trans_other(self) -> ActionUnit:
        pass
    
    @abstractmethod
    def trans_au(self,au: ActionUnit):
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """
        特殊语言的名字
        """
        pass
    