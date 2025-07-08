from PyQt6.QtWidgets import QMainWindow
from QtUI.views.rawUI.ui_rawMainWindow import Ui_MainWindow
from PyQt6.QtCore import pyqtSignal
import pyqtgraph as pg


#MVP中的view, 即用户直接看的GUI
class MainWindow(QMainWindow):
    #  ---------- 定义元类变量 ----------
    
    saveData_button_clicked = pyqtSignal(dict)
    timeSpan_choosed = pyqtSignal()
    date_selected = pyqtSignal(str)
    list_item_selected = pyqtSignal(dict)
    
    #  ---------- 开始初始化 ----------
    def __init__(self):
        super().__init__()
        
        self.MW = Ui_MainWindow()
        self.MW.setupUi(self)
        
        #  --- 赋值 ---
        self.CP = self.MW.capturePageBase
        self.MP = self.MW.menuPageBase
        
        #  ------ 接收 ------
        self.connectSignal()
        
        self.MW.stackedWidget.setCurrentWidget(self.MP)
    
    def connectSignal(self):
        self.CP.switchPage_button_clicked.connect(lambda p: self._on_page_switch_button_clicked(p))
        self.CP.saveData_button_clicked.connect(lambda d: self.saveData_button_clicked.emit(d))
        self.CP.date_selected.connect(lambda d: self.date_selected.emit(d))
        self.CP.list_item_selected.connect(lambda d: self.list_item_selected.emit(d))
        
        self.MP.switchPage_button_clicked.connect(lambda p: self._on_page_switch_button_clicked(p))
        self.MP.timeSpan_choosed.connect(self.timeSpan_choosed.emit)
        
    def _on_page_switch_button_clicked(self,page):
        if page == "menu":
            self.MW.stackedWidget.setCurrentWidget(self.MP)
        elif page == "capture":
            self.MW.stackedWidget.setCurrentWidget(self.CP)
    
    
    def updateMenu(self,timeUseRateStr,fourRealmRatioStr,extremeDataStr):
        self.MP.updateMenu(timeUseRateStr,fourRealmRatioStr,extremeDataStr)
        
    def fillCPData(self,data,au):
        self.CP.fillData(data,au)