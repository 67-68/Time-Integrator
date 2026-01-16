from PyQt6.QtWidgets import QApplication
import sys
from ti.services.dataService import DataService
from ti.view.MainWindow import MainWindow
from ti.core.mainCoordinator import MainCoorinator
from ti.services.serviceContainer import ServiceContainer
from ti.services.utils import load_qss, log_message

log_message("Application starting...")

class TimeIntegrator:
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
        self.app = QApplication(sys.argv)
        self.mainWindow = MainWindow()
        
        styleSheet = load_qss()
        self.app.setStyleSheet(styleSheet)
        self.ui = self.mainWindow.getUIs()
        self.ui["MW"] = self.mainWindow
        
        self.services = ServiceContainer()
        self.dataService: DataService = self.services.getService("DS")
        self.coordinator = MainCoorinator(self.services,self.mainWindow,self.ui)
