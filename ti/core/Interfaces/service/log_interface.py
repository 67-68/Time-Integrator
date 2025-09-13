from abc import ABC,abstractmethod


class ILogger(ABC):
    @property
    @abstractmethod
    def main_folder_path(self):
        pass
    
    @abstractmethod
    def log(self):
        pass