from PyQt6.QtWidgets import QMainWindow
from QtUI.views.rawUI.ui_rawMainWindow import Ui_MainWindow
from PyQt6.QtCore import pyqtSignal
import pyqtgraph as pg


#MVP中的view, 即用户直接看的GUI
class MainWindow(QMainWindow):
    #  ---------- 定义元类变量 ----------
    
    saveDataSignal = pyqtSignal(dict)
    
    #  ---------- 开始初始化 ----------
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        #  --- 赋值 ---
        self.CP = self.ui.capturePageBase
        self.MP = self.ui.menuPageBase
        
        #  ------ 接收 ------
        self.connectSignal()
        
        self.ui.stackedWidget.setCurrentWidget(self.MP)
    
    def connectSignal(self):
        self.CP.switchPageSignal.connect(lambda p: self._on_page_switch_button_clicked(p))
        
        self.CP.saveDataSignal.connect(lambda s: self.saveDataSignal.emit(s))
        
        self.MP.switchPageSignal.connect(lambda p: self._on_page_switch_button_clicked(p))
        
        
    def _on_page_switch_button_clicked(self,page):
        if page == "menu":
            self.ui.stackedWidget.setCurrentWidget(self.MP)
        elif page == "capture":
            self.ui.stackedWidget.setCurrentWidget(self.CP)
        
    

    
    

        
        # #  ------ 按钮 ------
        # buttons = {}
        
        # #  --- 主菜单按钮 ---
        # buttons["menu"] = [
        #     {"text":'input', "clicked":lambda: promptInput_FUNC(menuLabel,menuText,menuPage)}
        # ]
        
        # self.pages["menu"].leftToolFrame.coverToolButtons(buttons["menu"])
        
        # #  --- 展示界面按钮 ---
        # buttons["demo"] = [
        #         {"text":'DATE - simple data', "clicked":lambda: showSimpleData('Data/dateData.json',demonText)},
        #         {"text":'TYPE - action frequency', "clicked":lambda: setSwitchFrequency('Data/dateData.json',ActionType,demonText)},
        #         {"text":'TYPE - average time', "clicked":lambda: setAverageTime('Data/dateData.json',ActionType,demonText)},
        #         {"text":'ACTION - regist actions', "clicked":lambda: registAllAction_API('Data/dateData.json','Data/actionData.json')},
        #         {"text":'ACTION - show Ratio', "clicked":lambda: setTypeRatioToText_API('Data/actionData.json',ActionType,demonText)}
        # ]
        # self.pages["demo"].leftToolFrame.coverToolButtons(buttons["demo"])