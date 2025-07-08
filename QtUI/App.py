from Core.analysis.otherAnalysis import getActionUnit
from Core.dataAccess.dataManager import getData_API, saveData_API
from QtUI.views.MainWindow import MainWindow
from QtUI.presentors.menuPresenter import MenuPresenter
from PyQt6.QtWidgets import QApplication
import sys


class TimeIntegrator:
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        #  ---------- 初始化 ----------
        #  ----- 创建应用实例 ------
        self.app = QApplication(sys.argv)
        self.menuPresenter = MenuPresenter()
        
        #  ------ 创建UI ------
        self.mainWindow = MainWindow()
        
        #  ------ 应用状态 ------
        self.isDebugMode = False
        self.currentDate = None
        self.currentActionUnit = None #改成item
        self.currentData = getData_API("Data/dateData.json") #初始化的时候获取一份数据，在用户输入之后修改
        
        #  ------ 连接信号和槽 ------
        self.connectSignal()
    
    def connectSignal(self):
        self.mainWindow.timeSpan_choosed.connect(self._on_Time_Choosed)
        self.mainWindow.saveData_button_clicked.connect(lambda f:self._on_saveButton_clicked(f))
        self.mainWindow.date_selected.connect(self._on_date_selected)
        self.mainWindow.list_item_selected.connect(self._on_list_item_selected)

    def initialization(self):
        self.currentData = getData_API("Data/dateData.json") #初始化的时候获取一份数据，在用户输入之后修改
        pass
    
    def _on_list_item_selected(self,data):
        self.currentActionUnit = data
        self.initialization()
        self.mainWindow.fillCPData(self.currentData[self.currentDate],self.currentActionUnit)
        
    def _on_saveButton_clicked(self,actionUnits):
        #假设数据被validate过了
        date = self.currentDate
        self.currentData[date] = actionUnits
        saveData_API(self.currentData,"Data/dateData.json")
        self.initialization()         #初始化
        
        
    #UNIVERSAL; INPUT Str timeChoosed; OUTPUT the data that should update
    def _on_Time_Choosed(self,newTimeChoosed):
        actionUnits = getActionUnit(newTimeChoosed)
        if not actionUnits:
            return
        self.mainWindow.updateMenu(self.menuPresenter.processData(actionUnits))
        

    def _on_date_selected(self,date):
        allData = getData_API("Data/dateData.json")
        
        if date in allData:
            data = allData[date] #这个时候它是列表
            data = sorted(data, key=lambda au: au.get("start", ""))
            self.currentActionUnit = data[0]
        else:
            data = None
            self.currentActionUnit = None
            
        #  --- 存储状态 ---
        self.currentDate = date
        
        self.mainWindow.fillCPData(data,self.currentActionUnit)
        
        

