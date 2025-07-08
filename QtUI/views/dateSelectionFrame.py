from PyQt6.QtWidgets import QWidget,QListWidgetItem
from PyQt6.QtCore import pyqtSignal,Qt

from QtUI.views.rawUI.ui_rawDateSelectionFrame import Ui_dateSelection

class DateSelectionFrame(QWidget):
    dateSelected = pyqtSignal(str)
    list_item_selected = pyqtSignal(dict)
    
    def __init__(self, parent = None):
        super().__init__(parent)
        self.DSF = Ui_dateSelection()
        self.DSF.setupUi(self)
        
        #  ------ 初始化 ------
        self.calendar = self.DSF.calendarDateSelection
        self.list = self.DSF.actionUnitList
        
        #  ------ 绑定信号 ------
        self.calendar.selectionChanged.connect(self._on_calendar_selected)
        self.list.itemClicked.connect(self._on_list_item_clicked)
        
        stylesheet = """
            QListView::item:selected {
                /* 设置被选中项的样式 */
                background-color: #409EFF;
                color: white;
            }"""
            
        self.pos = None
        
        self.list.setStyleSheet(stylesheet)
    
    #  ------ 选择日期 ------
    def _on_calendar_selected(self):
        qDate = self.calendar.selectedDate()
        date = qDate.toString('yyyy-MM-dd')
        self.list.clear()
        self.dateSelected.emit(date)
        
    
    #  ------ 列表填充数据 ------
    def fillData(self,actionUnits = None,au = None):
        """
        这个函数用来初始化date selection 但是没有具体选择action Unit的情况
        """
        if actionUnits:
            self.fillListData(actionUnits)
        if au:
            self.list.setCurrentRow(0)
    
    def fillListData(self,data):
        """
        INPUT au; DISPLAY them on the list
        NOTICE: it will clear and reset all of the list items
        """
        itemList = []
        for au in data:                
            timeSpan = au.get("timeSpan","")
            text = f'{au["start"]}-{au["end"]} {au["action"]}({au["action_type"]}) {timeSpan}min'
            
            item = QListWidgetItem()
            item.setText(text)
            item.setData(Qt.ItemDataRole.UserRole,au)
            
            itemList.append(item)       #未来，这里可以加入自定义功能，自定义如何显示，显示什么

            
        #  --- 把字符串列表写入 QListWidget ---
        self.list.clear()
        for item in itemList:
            self.list.addItem(item)
            
    #  ------ 选择列表 ------
    def _on_list_item_clicked(self,item):        
        #  --- 获取数据 ---
        actionUnit = item.data(Qt.ItemDataRole.UserRole)
        
        #  --- 发送信号 ---
        self.list_item_selected.emit(actionUnit)   
    
    #  ------ 切换记录 ------
    def find_current_actionUnit_pos(self):
        return self.list.currentRow()
        
    def get_actionUnit_fromList(self,index):
        return self.list.item(index).data(Qt.ItemDataRole.UserRole) #要不然是index出问题导致抓取到空的，要不然是它出问题
    
    def get_actionUnit_listLength(self):
        return self.list.count()
    
    def find_item_by_au(self, au: dict) -> int | None:
        """
        返回列表中与 au 完全相等的项的行号；找不到返回 None
        """
        for i in range(self.list.count()):
            item_au = self.list.item(i).data(Qt.ItemDataRole.UserRole)
            if item_au == au:          # 必须逐项比较
                return i
        return None
    
    def switchItem(self,au):
        item = self.find_item_by_au(au)
        self.list.setCurrentRow(item)