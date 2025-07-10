from QtUI.views.rawUI.ui_rawPageSwitchFrame import Ui_pageswitchFrame
from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import pyqtSignal

class PageSwitchFrame(QFrame):
    switchPage_button_clicked = pyqtSignal(str)
    
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.PSF = Ui_pageswitchFrame()
        self.PSF.setupUi(self)
        
        #替换
        self.PSF.menuButton.clicked.connect(lambda: self._on_switchPage_button_clicked("menu"))
        self.PSF.captureButton.clicked.connect(lambda: self._on_switchPage_button_clicked("capture"))
        self.PSF.analysisButton.clicked.connect(lambda: self._on_switchPage_button_clicked("analysis"))
        
    def _on_switchPage_button_clicked(self,page):
        self.switchPage_button_clicked.emit(page)
        