from PyQt6.QtWidgets import QWidget

from PyQt6.QtCore import pyqtSignal
import uuid

from ti.UI.rawUI.ui_rawSettingPage import Ui_SettingPage

class SettingPage(QWidget):
    switchPage_button_clicked = pyqtSignal(str)
    
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.SP = Ui_SettingPage()
        self.SP.setupUi(self)
        
        self.SP.pageSwitchFrame.switchPage_button_clicked.connect(lambda f:self.switchPage_button_clicked.emit(f))
        
        #self.SP.uidButton.clicked.connect(self.re_construct_uuid)
        

        
        
        
        