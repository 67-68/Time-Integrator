from abc import ABC, abstractmethod
from PyQt6.QtCore import pyqtSignal
from ti.presenters.BasePresenter import BasePresenter


class IItemEditorPresenter(BasePresenter):
    save_data: pyqtSignal
    
    @abstractmethod
    def fill_data(self):
        pass
    
    @abstractmethod
    def _on_save_data(self):
        pass
    
    # new就不写了，或许可以用fill - save_data的框架？
    
    