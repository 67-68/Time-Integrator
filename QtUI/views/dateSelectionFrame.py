from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal

from QtUI.views.rawUI.ui_rawDateSelectionFrame import Ui_dateSelection
from PyQt6.QtGui import QBrush,QColor

class DateSelectionFrame(QWidget):
    dateSelected = pyqtSignal(str)
    actionUnitSelected = pyqtSignal(dict)
    
    def __init__(self, parent = None):
        super().__init__(parent)
        self.DSF = Ui_dateSelection()
        self.DSF.setupUi(self)
        
        #  ------ 初始化 ------
        self.calendar = self.DSF.calendarDateSelection
        self.list = self.DSF.actionUnitList
        self.recordList = [] #这里用list因为方便，后面人如果查找压力大可能改dict
        
        #  ------ 绑定信号 ------
        self.calendar.selectionChanged.connect(self._on_calendar_selected)
        self.list.itemClicked.connect(self._on_list_item_clicked)
        
    def _on_calendar_selected(self):
        qDate = self.calendar.selectedDate()
        date = qDate.toString('yyyy-MM-dd')
        self.list.clear()
        self.dateSelected.emit(date)
        
    
    #这里会接收到一天的数据
    def fillData(self,actionUnits):
        self.recordList.clear()
        
        if actionUnits:
            actionUnitsStrList = []
            for au in actionUnits:
                timeSpan = au.get("timeSpan","")
                text = f'{au["start"]}-{au["end"]} {au["action"]}({au["action_type"]}) {timeSpan}min'
                
                actionUnitsStrList.append(f'{au["start"]}-{au["end"]} {au["action"]}({au["action_type"]}) {timeSpan}min') #未来，这里可以加入自定义功能，自定义如何显示，显示什么

                self.recordList.append(au)
            #  --- 把字符串列表写入 QListWidget ---
            self.list.clear()
            self.list.addItems(actionUnitsStrList)
        
            #  --- 保存到recordDict方便查找 ---
            
        
    def _on_list_item_clicked(self,item):
        #  --- 获取text ---
        row = self.list.row(item)
        actionUnit = self.recordList[row]
        
        #  --- 清空本地数据 ---
        self.recordList = []
        
        #  --- 发送信号 ---
        self.actionUnitSelected.emit(actionUnit)
    
    def find_actionUnit_pos(self, actionUnit):
        """
        返回给定 actionUnit 在 self.recordList 中的序号（0‑基）。
        找不到则返回 -1。
        """
        for index, au in enumerate(self.recordList):
            if au == actionUnit:
                return index
        return -1
        
    def get_actionUnit_fromList(self,index):
        return self.recordList[index] #it should be reasonable, so no validation
    
    def get_actionUnit_listLength(self):
        return len(self.recordList)
        
    def dyeActionUnit(self,row,color):        
        item = self.list.item(row)                    # 拿到 QListWidgetItem
        item.setBackground(QBrush(QColor(color))) # 背景色
    
    def createNewRecord(self):
        self.recordList.append("")
        
    

        