from QtUI.views.dateSelectionFrame import DateSelectionFrame
from QtUI.views.editorFrame import EditorFrame
from QtUI.views.rawUI.ui_rawInputPage import Ui_inputPage
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal

class InputPage(QWidget):
    menuButtonClicked = pyqtSignal(bool)
    inputButtonClicked = pyqtSignal(bool)
    
    def __init__(self, parent = None):
        super().__init__(parent)

        #  ------ 初始化UI ------       
        self.inputPage = Ui_inputPage()
        self.inputPage.setupUi(self)
        
        #  ------ 创建子页面 ------
        self.dateSelectionFrame = DateSelectionFrame(self.inputPage.inputStackFrame)
        self.editorFrame = EditorFrame(self.inputPage.inputStackFrame)
        
        #  ----- 连接按钮和信号 ------
        #  --- 切换页面 ---
        self.inputPage.menuButton.clicked.connect(self.menuButtonClicked.emit)
        self.inputPage.inputButton.clicked.connect(self.inputButtonClicked.emit)
        
        #  --- 切换input widgets ---
        self.dateSelectionFrame.dateSelected.connect(self._on_date_selected)
        
    def _on_date_selected(self):
        self.inputPage.inputStackFrame.setCurrentIndex(self.editorFrame) 
        
        