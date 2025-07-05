from Core.dataAccess.dataManager import getData_API
from QtUI.views.rawUI.ui_rawCapturePage import Ui_CapturePage
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal

class CapturePage(QWidget):
    menuButtonClicked = pyqtSignal(bool)
    inputButtonClicked = pyqtSignal(bool)
    
    def __init__(self, parent = None):
        super().__init__(parent)

        #  ------ 初始化UI ------       
        self.inputPage = Ui_CapturePage()
        self.inputPage.setupUi(self)
        
        #  --- 快捷赋值 ---
        stack = self.inputPage.inputStackFrame
        
        #  ----- 连接按钮和信号 ------
        #  --- 切换页面 ---
        self.inputPage.menuButton.clicked.connect(self.menuButtonClicked.emit)
        self.inputPage.inputButton.clicked.connect(self.inputButtonClicked.emit)
        self.inputPage.editorFrameBase.confirmSignal.connect(lambda: stack.setCurrentWidget(self.inputPage.dateSelectionFrameBase))
        
        #  --- 切换input widgets ---
        self.inputPage.dateSelectionFrameBase.dateSelected.connect(self._on_date_selected)
        
    def _on_date_selected(self,date):
        self.inputPage.inputStackFrame.setCurrentWidget(self.inputPage.editorFrameBase)
        
        #  --- 填充数据 ---
        data = getData_API("Data/dateData.json")
        self.inputPage.editorFrameBase.fillData(date,data)
        
        
        
        