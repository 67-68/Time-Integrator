from abc import ABC,abstractmethod


class IInterventionEventSource(ABC):
    """
    干涉插件中负责输入的模块
    首先它需要提供一个方法来激活以及加载配置
    然后它需要一个方法来返回激活的事件
    它是否需要一个静态方法来标明它的身份？
    """
    
    @abstractmethod
    def initialize(self):
        """
        用来激活EventSource进程
        """
        pass
    
    @abstractmethod
    def publish_event(self):
        """
        条件满足之后
        用来发布一个事件
        """
        pass