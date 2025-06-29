from QtUI.views.rawUI.ui_rawPropertyEnterFrame import Ui_propertyEnterFrame
from PyQt6.QtWidgets import QFrame

class PropertyEnterFrame(QFrame):
    def __init__(self, parent = None):
        super().__init__(parent)
    
        self.propertyEnterFrame = Ui_propertyEnterFrame()
        self.propertyEnterFrame.setupUi(self)
        
        self.pe = self.propertyEnterFrame
        
        self.widget = {}
        
        self.widget["start"] = self.pe.startEdit
        self.widget["end"] = self.pe.endEdit
        self.widget["action_type"] = self.pe.actionTypeEdit
    
    #SPECIFIC; INPUT actionUnit, UPDATE data
    def fillData(self,actionData):
        self.pe.startEdit.setText(actionData["start"])
        self.pe.endEdit.setText(actionData["end"])
        self.pe.actionEdit.setText(actionData["action"])
        self.pe.actionTypeEdit.setText(actionData["action_type"])
        self.pe.actionDetailEdit.setText(actionData["actionDetail"])
    
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
