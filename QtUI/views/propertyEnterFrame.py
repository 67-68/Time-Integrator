from QtUI.views.rawUI.ui_rawPropertyEnterFrame import Ui_propertyEnterFrame
from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import pyqtSignal 

class PropertyEnterFrame(QFrame):
    #  --- 创建信号 ---
    propertyChanged = pyqtSignal(dict)
    
    def __init__(self, parent = None):
        super().__init__(parent)
    
        self.propertyEnterFrame = Ui_propertyEnterFrame()
        self.propertyEnterFrame.setupUi(self)
        
        self.pe = self.propertyEnterFrame
        
        self.widget = {}
        
        #  --- 打包控件 ---
        self.widget["start"] = self.pe.startEdit
        self.widget["end"] = self.pe.endEdit
        self.widget["action_type"] = self.pe.actionTypeEdit
        self.widget["actionDetail"] = self.pe.actionDetailEdit
        self.widget["action"] = self.pe.actionEdit
        
        #  --- 发送信号 ---
        for key in self.widget:
            self.widget[key].textChanged.connect(self._on_property_text_changed)
            
        
            
            
    """  ------ 速记和属性栏同步功能 ------ """
    #  ------ 上行事件传输 ------  
    def _on_property_text_changed(self):
        data = self.getData()
        self.propertyChanged.emit(data)
    
    
    #  ------ 下行指令承接 ------    
    #SPECIFIC; INPUT actionUnit, UPDATE data
    def fillData(self,actionData):
        if actionData is not None:
            self.pe.startEdit.setText(actionData["start"])
            self.pe.endEdit.setText(actionData["end"])
            self.pe.actionEdit.setText(actionData["action"])
            self.pe.actionTypeEdit.setText(actionData["action_type"])
            self.pe.actionDetailEdit.setText(actionData["actionDetail"])
        else:
            print("reset propeertyEnterFrame")
            self.pe.startEdit.setText("")
            self.pe.endEdit.setText("")
            self.pe.actionEdit.setText("")
            self.pe.actionDetailEdit.setText("")
            self.pe.actionTypeEdit.setText("")
            #TODO:importance和urgency的初始化
    
    def getData(self):
        actionUnit = {
            "start":"",
            "end":"",
            "action":"",
            "actionDetail":"",
            "action_type":"",
            "urgency":None,
            "importance":None
        }

        pe = self.propertyEnterFrame
        
        actionUnit = {
            "start": pe.startEdit.text(),
            "end": pe.endEdit.text(),
            "action": pe.actionEdit.text(),
            "actionDetail": pe.actionDetailEdit.text(),
            "action_type": pe.actionTypeEdit.text(),
            "urgency": pe.urgenCheckBox.isChecked(),  # 若 .ui 中有此对象
            "importance": pe.imporCheckBox.isChecked()
        }
        
        return actionUnit
    
    def showError(self,error):
        self.widget[error].setStyleSheet("background-color:#ffcccc;")


    def setWordBank(self,wordBank):
        self.pe.actionEdit.initialization(wordBank)
        
    def set_dropdown_prefix(self,key):
        self.pe.actionEdit.setPrefix(key)