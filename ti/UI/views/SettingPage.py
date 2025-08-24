from PyQt6.QtWidgets import QWidget

from PyQt6.QtCore import pyqtSignal
import uuid

from ti.UI.rawUI.ui_rawSettingPage import Ui_SettingPage
from ti.UI.widgets.other.BasicButton import BasicButton

class SettingPage(QWidget):
    switchPage_button_clicked = pyqtSignal(str)
    dialog_test = pyqtSignal()
    
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.SP = Ui_SettingPage()
        self.SP.setupUi(self)
        
        self.SP.pageSwitchFrame.switchPage_button_clicked.connect(lambda f:self.switchPage_button_clicked.emit(f))
        
        #self.SP.uidButton.clicked.connect(self.re_construct_uuid)
        
        dialogTestButton = BasicButton(self.SP.frame_2)
        dialogTestButton.setText("Test dialog")
        self.SP.horizontalLayout.addWidget(dialogTestButton)
        dialogTestButton.clicked.connect(self.dialog_test.emit)
        

        
        
        
        