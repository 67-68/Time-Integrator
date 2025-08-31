from abc import ABC,abstractmethod
from PyQt6.QtCore import pyqtSignal

class DetectorInterface(ABC):
    hook_pattern_detected = pyqtSignal(dict)
    pattern_detected = pyqtSignal(dict)
    
    @abstractmethod
    def process_event(self):
        pass