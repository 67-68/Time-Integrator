from PyQt6.QtWidgets import QWidget
from Core.dataAccess.dataAccess import getData, saveData
from QtUI.rawUI.ui_rawSettingPage import Ui_SettingPage
from PyQt6.QtCore import pyqtSignal
import uuid

class SettingPage(QWidget):
    switchPage_button_clicked = pyqtSignal(str)
    
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.SP = Ui_SettingPage()
        self.SP.setupUi(self)
        
        self.SP.pageSwitchFrame.switchPage_button_clicked.connect(lambda f:self.switchPage_button_clicked.emit(f))
        
        #self.SP.uidButton.clicked.connect(self.re_construct_uuid)
        
    def re_construct_uuid(self):
        data = getData("Data/dateData.json")
        for date in data:
            for au in data[date]:
                au["id"] = str(uuid.uuid4())
        
        saveData(data,"Data/dateData.json")
        
        
        