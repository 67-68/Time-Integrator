from PyQt6.QtCore import QObject
from abc import ABC, abstractmethod

from ti.services.utils import QtABCMeta


class BasePresenter(QObject, ABC, metaclass=QtABCMeta):
    """
    Presenter基类，所有Presenter都应该继承此类
    提供统一的接口和生命周期管理
    """

    def __init__(self, parent=None):
        super().__init__(parent)
    
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
    
    @property
    @abstractmethod
    def name(self):
        pass
    
    @property
    @abstractmethod
    def view(self):
        pass