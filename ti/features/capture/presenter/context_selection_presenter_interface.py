from abc import ABC, abstractmethod
from PyQt6.QtCore import pyqtSignal
from ti.features.capture.model.selection_condition import SelectionCondition
from ti.presenters.BasePresenter import BasePresenter


class IContextSelectionPresenter(BasePresenter):
    """
    数据模型背景库选择
    """
    selection_condition_changed: pyqtSignal
    # 这个信号会被Capture连接到Dataservice, 用来查询
    
    @abstractmethod
    def _on_selection_condition_change(self) -> SelectionCondition:
        """
        收集改变的数据，发送信号
        首先打包成为SelectionCondition对象
        
        Returns:
            SelectionCondition: _description_
        """
        pass
    
    @abstractmethod
    def get_selection_condition(self) -> SelectionCondition:
        """
        返回当前的selection condition

        Returns:
            SelectionCondition: _description_
        """
        pass
    