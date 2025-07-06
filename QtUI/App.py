#中间层，负责调用MainWindow中的函数和基础逻辑层面的函数，只要他们有交互
#即，presentor
from Core.analysis.otherAnalysis import getActionUnit, getExtremeData, getFourRealmRatio, getHighQualityRatio
from Core.dataAccess.dataManager import getData_API, saveData_API
from QtUI.views.MainWindow import MainWindow
from PyQt6.QtWidgets import QApplication
import sys


class TimeIntegrator:
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        #  ---------- 初始化 ----------
        #  ----- 创建应用实例 ------
        self.app = QApplication(sys.argv)
        
        #  ------ 创建UI ------
        self.mainWindow = MainWindow()
        
        #  ------ 应用状态 ------
        self.isDebugMode = False
        
        #  ------ 连接信号和槽 ------
    
    def connectSignal(self):
        #self.mainWindow.timeSpanChoosed.connect(self._on_Time_Choosed)
        self.mainWindow.saveDataSignal.connect(lambda f:self.saveData(f))

    def initialization(self):
        #self.mainWindow.timeSpanChoosed.emit(self.mainWindow.ui.timeChooser.currentText())
        pass
        
    def saveData(self,saveDataPack):
        #假设数据被validate过了
        date = saveDataPack["date"]
        actionUnits = saveDataPack["data"]
        
        allData = getData_API("Data/dateData.json")
        allData[date] = actionUnits
        
        saveData_API(allData,"Data/dateData.json")
        
        #初始化
        self.initialization()
        
        
    #UNIVERSAL; INPUT Str timeChoosed; OUTPUT the data that should update
    def _on_Time_Choosed(self,newTimeChoosed):
        #  --- 首先找到actionUnit ---
        actionUnits = getActionUnit(newTimeChoosed)
        if not actionUnits:
            #TODO:建立一个错误显示体系。不同等级 showError("there is no recording of today") 
            return
        
        #  --- 然后调用函数处理actionUnit ---
        timeUseRate = getHighQualityRatio(actionUnits)
        fourRealmRatio = getFourRealmRatio(actionUnits)
        extremeData = getExtremeData(actionUnits)
        
        #  --- 整理好数据，使其可以直接阅读 ---
        timeUseRateStr = self.organizeTimeRate(timeUseRate)
        fourRealmRatioStr = self.organizeRealmRatio(fourRealmRatio)
        extremeDataStr = self.organizeExtremeData(extremeData)
        
        #  --- 输出到view ---
        self.mainWindow.updateMenu(timeUseRateStr,fourRealmRatioStr,extremeDataStr)
        
        #在这里调用各种代码处理，首先找到时间段的actionUnit, 然后调用逻辑处理，最后输出为整理好的数据，调用view中的函数update
    
    #UNIVERSAL; INPUT time ratio data; OUTPUT str
    def organizeTimeRate(self,data):
        return int(data) * 100
    
    def organizeRealmRatio(self,ratios):
        for key in ratios:
            ratios[key] = (ratios[key]*100)
        return ratios
    
    def organizeExtremeData(self,extremeData):
        output = ""
        for key in extremeData:
            data = extremeData[key]
            #我很奇怪为什么有些数据有date有些没有...无论如何我得想另一个办法找到date...我还是给所有数据都popularize date好了
            date = data["date"]
            start = data["start"]
            end = data["end"]
            important = "important"
            if not data["importance"]:
                important = "not " + important
            urgent = "urgent"
            if not data["urgency"]:
                urgent = "not " + urgent
            
            output += f'in {date},{start}-{end},you do the longest time of {important} and {urgent} things \n'
            
        return output
            