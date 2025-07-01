from Core.analysis.APITools import getAutoCompletion_API
from QtUI.views.rawUI.ui_rawInputEnterFrame import Ui_inputEnterFrame
from PyQt6.QtWidgets import QFrame
from QtUI.presentors.translator import Translator
from PyQt6.QtCore import QSignalBlocker,QTimer

actionDataLoc = "Data/actionData.json"

class InputEnterFrame(QFrame):
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.inputEnterFrame = Ui_inputEnterFrame()
        self.inputEnterFrame.setupUi(self)
        
        #  --- 赋值好使用 ---
        self.pe = self.inputEnterFrame.propertyEnterFrameBase
        self.fe = self.inputEnterFrame.fastEnterFrameBase
        
        #  --- 创建wordBank ---
        wordBank = getAutoCompletion_API(actionDataLoc)
        self.fe.setWordBank(wordBank)
        
        #  --- 创建presentor实例 ---
        self.translator = Translator()
            
        #  --- 连接信号 ---
        self.pe.propertyChanged.connect(lambda: self._on_text_changed("property"))
        self.fe.fastTextChanged.connect(lambda d: self._on_text_changed("fast",d))
    
    def _on_text_changed(self,pattern,data_from_signal = None):
        if pattern == "property":
            with QSignalBlocker(self.fe.fastEnterFrame.fastEntry):
                data = self.pe.getData()
                fastData = self.translator.properToFast(data)
                self.fe.fillData(fastData)
        
        elif pattern == "fast":
            QTimer.singleShot(0,lambda: self.updatePropertyFrameLater(data_from_signal))
        
        
    def updatePropertyFrameLater(self,data_From_Signal):
        with QSignalBlocker(self.pe.propertyEnterFrame.propertyEntries):
                self.pe.fillData(data_From_Signal) #它并不需要被translate，而是直接修改propertyFrame
    
    def fillData(self,actionUnit):
        #  --- 拆包 ---
        text = self.translator.properToFast(actionUnit)
        
        
        self.pe.fillData(actionUnit)
        self.fe.fillData(text)
        
    def getData(self):
        actionUnit = self.inputEnterFrame.propertyEnterFrameBase.getData()
        return actionUnit
        
        
    
    #SPECIFIC; INPUT error; UPDATE propertyFrame to show the error
    def showError(self,error):
        self.inputEnterFrame.propertyEnterFrameBase.showError(error)