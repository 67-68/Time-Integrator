
from abc import ABC,abstractmethod


class IPathRegisterProvider(ABC):
    """
    这个类用来表示继承它的类可以提供一个symbol register 
    用来支持符号路径的翻译和yaml使用
    无论是不是插件类

    Args:
        ABC (_type_): _description_
    """
    
    @staticmethod
    @abstractmethod
    def register_class(self):
        """
        返回一个register类
        """
        pass