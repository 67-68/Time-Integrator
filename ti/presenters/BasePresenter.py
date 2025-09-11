from PyQt6.QtCore import QObject
from abc import ABC, abstractmethod


class BasePresenter(ABC):
    """
    Presenter基类，所有Presenter都应该继承此类
    提供统一的接口和生命周期管理
    """
    
    def __init__(self, parent=None):
        super().__init__()
    
    @abstractmethod
    def initialize(self):
        """初始化Presenter"""
        pass
    
    @abstractmethod
    def shutdown(self):
        """关闭Presenter，清理资源"""
        pass
    
    def get_widget(self):
        """获取管理的Widget（如果适用）"""
        return None