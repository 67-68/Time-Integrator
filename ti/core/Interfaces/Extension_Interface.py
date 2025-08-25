from abc import ABC,abstractmethod

from ti.core.eventBus import EventBus

class ExtensionInterface(ABC):    
    @property
    @abstractmethod
    def name(self) -> str:
        """_summary_
        这是一个抽象的返回名字方法
        在实现的时候不需要把类属性定义一个Name
        而是把方法返回值直接return name
        Returns:
            str: 名字
        """
        pass
    
    @abstractmethod
    def initialize(self,eventBus: EventBus):
        """_summary_
        初始化方法，会提供一个EventBus供订阅
        在这里开始插件初始化
        Args:
            eventBus (EventBus): _description_
        """
        pass
    
    @abstractmethod
    def shutdown(self):
        """_summary_
        关闭方法，在这里关闭插件
        删除创建的实例
        """
        pass
    