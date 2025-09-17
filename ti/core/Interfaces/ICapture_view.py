


from abc import abstractmethod
from ti.services.utils import QtABCMeta


class ICaptureView(QtABCMeta):
    @abstractmethod
    def fill(self):
        pass
    
    @abstractmethod
    def initialize(self):
        pass
    
    @abstractmethod
    def clear(self):
        pass
    
    @abstractmethod
    def get_data(self):
        pass
    
    @abstractmethod
    def _on_save(self):
        pass