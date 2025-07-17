import os
from Core.analysis.matchers import get_time_from_str
from Core.analysis.otherAnalysis import getActionUnit, updateActionList
from Core.dataAccess.dataManager import getData, saveData
from Core.utils import resource_path
from QtUI.views.MainWindow import MainWindow
from QtUI.presenters.menuPresenter import MenuPresenter
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
        
        self.app.setStyleSheet(load_qss())
        
        #  ------ 应用状态 ------
        self.isDebugMode = False
        self.currentDate = None
        self.currentActionUnit = None #改成item
        self.currentData = getData("Data/dateData.json") #初始化的时候获取一份数据，在用户输入之后修改
        
        #  ------ 连接信号和槽 ------
        self.connectSignal()
        
        #  ------ 初始化，传递依赖 ------
        self.initialization()
    
    def connectSignal(self):
        self.mainWindow.timeSpan_choosed.connect(self._on_Time_Choosed)
        self.mainWindow.saveData_button_clicked.connect(lambda f:self._on_saveButton_clicked(f))
        self.mainWindow.date_selected.connect(self._on_date_selected)
        self.mainWindow.list_item_selected.connect(self._on_list_item_selected)
            
    def _on_list_item_selected(self,data):
        self.currentActionUnit = data
        # 更新 CapturePage，使编辑区与新选中的 actionUnit 同步
        self.mainWindow.switchCPData(data)
        
    def _on_saveButton_clicked(self,actionUnit):
        #假设数据被validate过了
        date = self.currentDate
        if date not in self.currentData:
            self.currentData[date] = []
        
        actionUnit["date"] = date
        actionUnit["timeSpan"] = get_time_from_str(actionUnit["end"]) - get_time_from_str(actionUnit["start"])
        
        self.currentData[date].append(actionUnit)
        
        updateActionList(actionUnit)
        saveData(self.currentData,"Data/dateData.json")
        self.initialization()         #初始化
        
        
    #UNIVERSAL; INPUT Str timeChoosed; OUTPUT the data that should update
    def _on_Time_Choosed(self,newTimeChoosed):
        actionUnits = getActionUnit(newTimeChoosed)
        if not actionUnits:
            return
        self.mainWindow.updateMenu(self.menuPresenter.processData(actionUnits))
        

    def _on_date_selected(self,date):
        allData = getData("Data/dateData.json")
        
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
    
        
    def initialization(self): 
        """_summary_
        初始化，传递依赖，刷新所有需要数据的功能
        """
        #  --- 获取数据 ---
        self.currentData = getData("Data/dateData.json") 
        
        #  --- 传递依赖 ---
        self.mainWindow.initialization(self.currentData)
        

def load_qss():
    qss_path = resource_path("assets/styles/main.qss")
    with open(qss_path, 'r', encoding='utf-8') as f:
        return f.read()