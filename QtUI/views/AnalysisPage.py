from QtUI.views.rawUI.ui_rawAnalysisPage import Ui_analysisPage
from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import pyqtSignal

class AnalysisPage(QFrame):
    switchPage_button_clicked = pyqtSignal(str)
    
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.AP = Ui_analysisPage()
        self.AP.setupUi()
        
        self.AP.pageSwitchFrameBase.switchPage_button_clicked.connect(lambda f:self.switchPage_button_clicked.emit(f))