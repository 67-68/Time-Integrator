from PyQt6.QtWidgets import QMainWindow

from PyQt6.QtCore import pyqtSignal
import pyqtgraph as pg

from ti.features.core_capture.CapturePage import New_CapturePage
from ti.model.action_unit import ActionUnit
from ti.features.core_capture.capture_page_presenter import CapturePagePresenter
from ti.view.rawUI.ui_rawMainWindow import Ui_MainWindow



#MVP中的view, 即用户直接看的GUI
class MainWindow(QMainWindow):
    #  ---------- 定义元类变量 ----------
    
    saveData_button_clicked = pyqtSignal(ActionUnit)
    timeSpan_choosed = pyqtSignal()
    date_selected = pyqtSignal(str)
    list_item_selected = pyqtSignal(ActionUnit)
    new_button_selected = pyqtSignal()
    
    #  ---------- 开始初始化 ----------
    def __init__(self):
        super().__init__()
        
        self.MW = Ui_MainWindow()
        self.MW.setupUi(self)
        
        #  --- 赋值 ---
        self.createUI()
        
        #  ------ 接收 ------
        self.connectSignal()
        
        self.MW.stackedWidget.setCurrentWidget(self.MP)
        
    def getUIs(self):
        """
        这个函数返回所有的UI实例
        包括CP, AP和MP
        """
        return self.ui
    
    def getUI(self,ui: str):
        """_summary_
        返回单个ui
        可选的有AP,CP,MP
        Args:
            ui (str): ui的名称
        """
        return self.ui[ui]
    
    def createUI(self):
        """_summary_
        这个函数创建UI的引用
        """
        self.CP = self.MW.capturePageBase
        self.MP = self.MW.menuPageBase
        self.AP = self.MW.analysisPageBase
        self.SP = self.MW.settingPage
        
        
        self.ui = {
            "CP": self.CP,
            "AP": self.AP,
            "MP": self.MP,
            "SP": self.SP
        }
        
    def connectSignal(self):
        # 连接capture page信号 - 根据capture page类型采用不同的连接方式
        if hasattr(self.CP, 'switchPage_button_clicked'):
            # 旧的capture page信号连接
            self.CP.switchPage_button_clicked.connect(lambda p: self._on_page_switch_button_clicked(p))
            self.CP.saveData_button_clicked.connect(lambda d: self.saveData_button_clicked.emit(d))
            self.CP.date_selected.connect(lambda d: self.date_selected.emit(d))
            self.CP.list_item_selected.connect(lambda d: self.list_item_selected.emit(d))
            self.CP.new_button_selected.connect(self.new_button_selected.emit)
        else:
            # 新的capture page基于IPageView，只有page_first_clicked信号
            # 具体的业务逻辑由capture page presenter处理
            print("新的capture page使用IPageView接口，业务信号由presenter处理")
        
        # 连接其他页面的信号
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
    

    