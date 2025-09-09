from enum import Enum
from abc import ABC,abstractmethod

class PathRegisterInterface(ABC):
    @property
    @abstractmethod
    def domain(self):
        """
        用来登记这个register负责哪一个模块
        """
        pass
    
    @property
    @abstractmethod
    def class_file_path(self):
        """
        存储类yaml符号类对应文件的路径
        """
        pass
    
    @property
    @abstractmethod
    def class_method_file_path(self):
        """
        存储类yaml符号类方法对应文件的路径
        """
        pass
    
    @property
    @abstractmethod
    def function_file_path(self):
        """
        存储函数yaml符号对应文件的路径
        """
        pass
    
    @property
    @abstractmethod
    def enum_file_path(self):
        """
        存储enum类yaml符号对应文件的路径
        """
        pass
    
    
    
    @abstractmethod
    def regist_symbol_path(self):
        """
        用来登记一个符号进入注册表的变量库
        内部存储为symbol_model dataclass
        """
        pass

    @abstractmethod
    def get_symbol_path(self):
        """
        根据id获取symbol
        """
        pass
    
    @abstractmethod
    def search_symbol_data(self):
        """
        根据条件搜索symbol
        返回所有搜索到的symbol model
        """
        pass
    
    @abstractmethod
    def get_symbol_model(self):
        """
        返回这个symbol相关的信息
        返回dataclass: symbol model
        """
    
    @abstractmethod
    def load_data(self):
        """
        在这里加载存储的三个model文件的数据
        存入类变量
        """
        pass
    
