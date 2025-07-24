from PyQt6.QtWidgets import QMainWindow
from QtUI.rawUI.ui_rawMainWindow import Ui_MainWindow
from PyQt6.QtCore import pyqtSignal
import pyqtgraph as pg


#MVP中的view, 即用户直接看的GUI
class MainWindow(QMainWindow):
    #  ---------- 定义元类变量 ----------
    
    saveData_button_clicked = pyqtSignal(dict)
    timeSpan_choosed = pyqtSignal()
    date_selected = pyqtSignal(str)
    list_item_selected = pyqtSignal(dict)
    new_button_selected = pyqtSignal()
    
    #  ---------- 开始初始化 ----------
    def __init__(self):
        super().__init__()
        
        self.MW = Ui_MainWindow()
        self.MW.setupUi(self)
        
        #  --- 赋值 ---
        self.CP = self.MW.capturePageBase
        self.MP = self.MW.menuPageBase
        self.AP = self.MW.analysisPageBase
        self.SP = self.MW.settingPage
        
        #  ------ 接收 ------
        self.connectSignal()
        
        self.MW.stackedWidget.setCurrentWidget(self.MP)
        
    
    def connectSignal(self):
        self.CP.switchPage_button_clicked.connect(lambda p: self._on_page_switch_button_clicked(p))
        self.CP.saveData_button_clicked.connect(lambda d: self.saveData_button_clicked.emit(d))
        self.CP.date_selected.connect(lambda d: self.date_selected.emit(d))
        self.CP.list_item_selected.connect(lambda d: self.list_item_selected.emit(d))
        self.CP.new_button_selected.connect(self.new_button_selected.emit)
        
        self.MP.switchPage_button_clicked.connect(lambda p: self._on_page_switch_button_clicked(p))
        self.MP.timeSpan_choosed.connect(self.timeSpan_choosed.emit)
        
        self.AP.switchPage_button_clicked.connect(lambda p: self._on_page_switch_button_clicked(p))
        
        self.SP.switchPage_button_clicked.connect(lambda p: self._on_page_switch_button_clicked(p))
        
    def _on_page_switch_button_clicked(self,page):
        if page == "menu":
            self.MW.stackedWidget.setCurrentWidget(self.MP)
        elif page == "capture":
            self.MW.stackedWidget.setCurrentWidget(self.CP)
        elif page == "analysis":
            self.MW.stackedWidget.setCurrentWidget(self.AP)
        elif page == "setting":
            self.MW.stackedWidget.setCurrentWidget(self.SP)
    
    
    def updateMenu(self,timeUseRateStr,fourRealmRatioStr,extremeDataStr):
        self.MP.updateMenu(timeUseRateStr,fourRealmRatioStr,extremeDataStr)
        
    def fillCPData(self,data,au):
        """_summary_
        this function will clear and reconstruct the overall actionUnit list.
        It will also reset the editor page
        """
        self.CP.fillData(data,au)
        
    def switchCPData(self,au):
        """_summary_
        this function will try to find the item that containing data matches au and select it, rather then clear and reset it
        it will also reset editor page
        """
        self.CP.switchData(au)
    
    def initialization(self,data):
        """_summary_
        传递依赖
        """
        self.AP.initialization(data)
    