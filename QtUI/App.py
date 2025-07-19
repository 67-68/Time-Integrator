import os
from Core.analysis.matchers import get_time_from_str
from Core.analysis.otherAnalysis import getActionUnit, updateActionList
from Core.dataAccess.dataManager import createNewData, getData, saveData
from Core.utils import log_message, resource_path
from QtUI.views.MainWindow import MainWindow
from QtUI.presenters.menuPresenter import MenuPresenter
from PyQt6.QtWidgets import QApplication
import sys
from Core.Definitions import TODAY
        

log_message("Application starting...")

class TimeIntegrator:
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        #  ---------- 初始化 ----------
        #  ----- 创建应用实例 ------
        self.app = QApplication(sys.argv)
        self.menuPresenter = MenuPresenter()
        
        #  ------ 创建UI ------
        self.mainWindow = MainWindow()
        log_message("MainWindow instantiated.")
        
        log_message("Loading QSS...")
        styleSheet = load_qss()
        log_message("QSS loaded successfully.")
        
        self.app.setStyleSheet(styleSheet)
        log_message("Stylesheet applied.")
        
        #  ------ 持有的状态 ------
        self.isDebugMode = False
        self.currentDate = None
        self.currentActionUnit = None 
        self.currentData = getData("Data/dateData.json") #初始化的时候获取一份数据，在用户输入之后修改
        self.previousAU = None
        
        #  ------ 连接信号和槽 ------
        self.connectSignal()
        
        #  ------ 初始化，传递依赖 ------
        self.refreshWidget()
        
        #  ------ 初始化今天 -----
        self._on_date_selected(TODAY)
    
    def connectSignal(self):
        self.mainWindow.timeSpan_choosed.connect(self._on_Time_Choosed)
        self.mainWindow.saveData_button_clicked.connect(lambda f:self._on_saveButton_clicked(f))
        self.mainWindow.date_selected.connect(self._on_date_selected)
        self.mainWindow.list_item_selected.connect(self._on_list_item_selected)
        self.mainWindow.new_button_selected.connect(self.createNewRecord)
    
    def createNewRecord(self):
        """
        这个函数用来创建新的记录
        新的记录不会被保存到正式的数据状态中
        直到它被保存
        """
        self.previousAU = self.currentActionUnit
        
        nR = createNewData()
        nR["date"] = self.currentDate
        self.currentActionUnit = nR
        if self.currentDate not in self.currentData:
            self.currentData[self.currentDate] = []
        #新数据暂时不放进总的数据中，等到修改之后再检测
        
        self._on_list_item_selected(nR)
        
    
    def _on_list_item_selected(self,data):
        """
        这个函数用来更新
        当QlistWidget被选中的时候
        """
        self.previousAU = self.currentActionUnit
        #把新数据放上去
        
        self.currentActionUnit = data
        
        # 更新 CapturePage，使编辑区与新选中的 actionUnit 同步
        self.mainWindow.switchCPData(data)
        
    def _on_saveButton_clicked(self,actionUnit):
        self.saveData(actionUnit)
    
    def saveData(self,actionUnit):
        """
        保存一条数据
        准确来说，是修改原本的数据
        把相同uid的数据叠加上去
        （同时，保存之前的数据状态)
        """
        date = self.currentDate
        if date not in self.currentData:
            self.currentData[date] = []
        
        actionUnit["date"] = date
        # 这里的id没有必要，因为新建的时候就有了id
        
        data = self.currentData[date]
        
        assign = None
        #这里是针对一般数据的修改模块
        for i in range (len(data)):
            if data[i]["id"] == actionUnit["id"]:
                data[i] = actionUnit
                assign = True
                break
        if assign != True:
            data.append(actionUnit)
        
        self.currentData[date] = data
        
        updateActionList(actionUnit)
        saveData(self.currentData,"Data/dateData.json")
        self.refreshWidget()         #初始化
        self.mainWindow.fillCPData(data,self.currentActionUnit)
        
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
    
    def refreshWidget(self): 
        """_summary_
        初始化，传递依赖，刷新所有需要数据的功能
        """
        #  --- 获取数据 ---
        self.currentData = getData("Data/dateData.json") 
        
        #  --- 传递依赖 ---
        self.mainWindow.initialization(self.currentData)
        

def load_qss():
    log_message("Entering load_qss function.")
    
    qss_path = resource_path("assets/styles/main.qss")
    log_message(f"Resolved QSS path to: {qss_path}")
    
    try:
        with open(qss_path, 'r', encoding='utf-8') as f:
            log_message("Successfully read QSS file content.")
            return f.read()
    except Exception as e:
        log_message(f"!!!!!!!! FAILED to read QSS file: {e}")
        raise e
    