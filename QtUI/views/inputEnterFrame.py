from Core.translation.propertyTranslation import transPropToFast_API
from QtUI.views.rawUI.ui_rawInputEnterFrame import Ui_inputEnterFrame
from PyQt6.QtWidgets import QFrame

class InputEnterFrame(QFrame):
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.inputEnterFrame = Ui_inputEnterFrame()
        self.inputEnterFrame.setupUi(self)
    
    def fillData(self,actionUnit):
        #  --- 拆包 ---
        self.inputEnterFrame.propertyEnterFrameBase.fillData(actionUnit)
        
        text = transPropToFast_API(actionUnit)
        self.inputEnterFrame.fastEnterFrameBase.fillData(text)
        
    def getData(self):
        actionUnit = self.inputEnterFrame.propertyEnterFrameBase.getData()
        return actionUnit
        
        
    
    #SPECIFIC; INPUT error; UPDATE propertyFrame to show the error
    def showError(self,error):
        self.inputEnterFrame.propertyEnterFrameBase.showError(error)