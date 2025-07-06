from Core.dataAccess.dataManager import getData_API
from QtUI.views.rawUI.ui_rawCapturePage import Ui_CapturePage
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal

class CapturePage(QWidget):
    switchPageSignal = pyqtSignal(str)
    saveDataSignal = pyqtSignal(dict)
    
    def __init__(self, parent = None):
        super().__init__(parent)

        #  ------ 初始化UI ------       
        self.CP = Ui_CapturePage()
        self.CP.setupUi(self)
        self.DSF = self.CP.dateSelectionFrameBase
        self.EF = self.CP.editorFrameBase
        self.WF = self.CP.welcomeFrame
        
        self.CP.stackedWidget.setCurrentWidget(self.WF)
        
        #  ----- 上行事件接收 ------
        #  --- 切换页面 ---
        self.CP.menuButton.clicked.connect(lambda: self.switchPageSignal.emit("menu"))
        self.CP.inputButton.clicked.connect(lambda: self.switchPageSignal.emit("capture"))
        
        #  --- dateSelection ---
        self.DSF.dateSelected.connect(self._on_date_selected)
        self.DSF.actionUnitSelected.connect(self._on_actionUnit_selected)
        
        self.CP.splitter.setSizes([300, 1000])        # 绝对像素
        
        #  --- EditorFrame ---
        self.EF.changeActionUnit.connect(lambda i: self._on_change_actionUnit(i))
        self.EF.saveDataSignal.connect(lambda s: self._on_save_button_clicked(s))
        
        
        #  --- 存储状态，但只是一个简单的指示器 ---
        self.currentDate = None
        self.currentActionUnit = None
        
    def _on_save_button_clicked(self,saveDataPack):
        saveDataPack["date"] = self.currentDate
        self.saveDataSignal.emit(saveDataPack)
        
    
    def _on_change_actionUnit(self,index):
        #首先确认不是新建
        if index is not 0:
            #由于传过来的是一个数字，首先我需要找到当前找到是第几项
            pos = self.DSF.find_actionUnit_pos(self.currentActionUnit)
            len = self.DSF.get_actionUnit_listLength()
            #然后设置下一项，顺便滚动
            if index is 1:
                if pos + 1 >= len:
                    idx = 0
                else:
                    idx = pos + 1
            elif index is -1:
                if pos == 0:
                    idx = len 
                else:
                    idx = pos - 1
            
            actionUnit = self.DSF.get_actionUnit_fromList(idx)
        elif index == 0:
            actionUnit = None
            
        self._on_actionUnit_selected(actionUnit)
            
    #在收到date之后，要获取数据，排序，传回给actionUnitList和editorFrame
    def _on_date_selected(self,date):
        #  --- 获取数据 ---
        allData = getData_API("Data/dateData.json")
        
        if date in allData:
            data = allData[date] #这个时候它是列表
            data = sorted(data, key=lambda au: au.get("start", ""))
        else:
            data = None
            
        #  --- 存储状态 ---
        self.currentDate = date
        
        #  --- 指令下行 ---
        self.DSF.fillData(data)
        
        #  --- 填充editorFrame ---
        if data:
            self.fillEditorFrame(data[0])
        else:
            self.fillEditorFrame(None)
        
        #  --- 切换为editorFrame ---
        self.CP.stackedWidget.setCurrentWidget(self.EF)
    
    def _on_actionUnit_selected(self,actionUnit):
        #  --- 初始化List ---
        self.currentActionUnit = actionUnit
        
        #  --- 获取当前actionUnits ---
        allData = getData_API("Data/dateData.json")
        data = allData.get(self.currentDate,"") #这个时候它是列表
        data = sorted(data, key=lambda au: au.get("start", ""))
        
        #  --- 传输给list ---
        self.DSF.fillData(data)
        
        #  --- 传输给EditorFrame ---
        self.fillEditorFrame(actionUnit)
        
        if actionUnit:
            self.setCurrentItemColor("#409EFF")
        else:
            self.DSF.createNewRecord()
    
    
    
    #只有它被填充了数据才显示，否则隐藏到欢迎界面
    def fillEditorFrame(self,actionUnit):
        if actionUnit:
            self.EF.fillData(actionUnit)
        else:
            #  --- 手动初始化欢迎界面 ---       已经选择日期但是没有记录
            self.EF.setTutorialLabels()
        
    
    def setCurrentItemColor(self,color):
        row = self.DSF.find_actionUnit_pos(self.currentActionUnit)
        self.DSF.dyeActionUnit(row,color)
        
        
            