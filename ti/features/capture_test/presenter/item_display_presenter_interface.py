from abc import ABC, abstractmethod
from ti.presenters.BasePresenter import BasePresenter
from PyQt6.QtCore import pyqtSignal


class IItemDisplayPresenter(BasePresenter,ABC):
    item_selected: pyqtSignal

    @abstractmethod
    def fill_data(self):
        pass
    
    @abstractmethod
    def _on_item_selected(self):
        pass
    
    @abstractmethod
    def add_data(self,model_data):
        pass
    
