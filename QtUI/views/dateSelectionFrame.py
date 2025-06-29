from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal

from Core.dataAccess.dataManager import getData_API
from QtUI.views.rawUI.ui_rawDateSelectionFrame import Ui_dateSelection

from PyQt6.QtCore import QDate



class DateSelectionFrame(QWidget):
    dateSelected = pyqtSignal(str)
    
    def __init__(self, parent = None):
        super().__init__(parent)
        self.dateSelectionFrame = Ui_dateSelection()
        self.dateSelectionFrame.setupUi(self)
        
        #  ------ 初始化 ------
        #  --- 输入框 ---
        self.dateSelectionFrame.dateTimeEdit.setDisplayFormat("yyyy-MM-dd")
        self.dateSelectionFrame.dateTimeEdit.setDate(QDate.currentDate())
        
        #  ------ 绑定信号 ------
        self.dateSelectionFrame.dateTimeEdit.dateChanged.connect(self._on_dateTimeEdit_enter)
        self.dateSelectionFrame.newRecordButton.clicked.connect(self._on_dateTimeConfirm)
    
    
    # def _on_enter_entered(self,obj,event):
    #     #  ------ 判断enter 是否被entered ------
    #     if event.type() == QEvent.Type.KeyPress and \
    #         event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            
    #         #  ------ 判断在哪个控件 ------
    #         focus = self.focusWidget()          # 这里用 self.focusWidget 也行
    #         self.getDate(focus)
            
    #         return True
        
    # def getDate(self,widget):
    #     if widget == self.dateSelectionFrame.dateTimeEdit:
        
    #     if widget == self.dateSelectionFrame.calendarWidget:
        
        
    def _on_dateTimeEdit_enter(self,q_date):
        date = q_date.toString("yyyy-MM-dd")
        data = getData_API("Data/dateData.json")
        
        #  --- 判断用户是否输入完成 ---
        if not q_date.isValid():
            return
        
        #  --- 传递信号 ---
        if date in data:
            self.dateSelected.emit(date)
    
    def _on_dateTimeConfirm(self):
        date = self.dateSelectionFrame.dateTimeEdit.text()
        q_date = QDate.fromString(date,"yyyy-MM-dd")
        
        #  --- 判断是否valid ---
        if not q_date.isValid():
            return
        
        #  --- 传递信号 ---
        self.dateSelected.emit(date)