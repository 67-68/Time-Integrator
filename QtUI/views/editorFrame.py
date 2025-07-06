from Core.analysis.APITools import getTimeSpan_API
from QtUI.views.rawUI.ui_rawEditorFrame import Ui_editorFrame
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal
from QtUI.presentors.inputValidationPresentor import InputValidation

class EditorFrame(QWidget):    
    
    saveDataSignal = pyqtSignal(dict)
    changeActionUnit = pyqtSignal(int)
    
    def __init__(self, parent = None):
        super().__init__(parent)
    
        self.editorFrame = Ui_editorFrame()
        self.editorFrame.setupUi(self)
                
        #  --- 关联回调函数 ---
        self.editorFrame.leftSwitchButton.clicked.connect(lambda: self.changeActionUnit.emit(-1))
        self.editorFrame.rightSwitchButton.clicked.connect(lambda: self.changeActionUnit.emit(1))
        self.editorFrame.saveButton.clicked.connect(self._on_confirmButton_clicked)
        self.editorFrame.createNewButton.clicked.connect(lambda: self.changeActionUnit.emit(0))
        
        #  --- 创建检验对象 ---
        self.validation = InputValidation()
        
        #  --- 
        self.EF = self.editorFrame
        self.IEF = self.editorFrame.inputEnterFrameBase

    
    #SPECIFIC; DETECT confirmButton; VALIDATE, COLLECT data and EMIT a signal to presentor
    def _on_confirmButton_clicked(self):
        actionUnits = self.collectData()
        actionUnits["timeSpan"] = getTimeSpan_API(actionUnits["start"],actionUnits["end"])
        
        saveDataPack = {}
        saveDataPack["data"] = actionUnits
        
        # 把包含 data 键的完整数据包发射出去
        self.saveDataSignal.emit(saveDataPack)
        
    #SPECIFIC; Collect data from stackedwidget, OUTPUT them as list of actionUnit
    def collectData(self):
        return self.IEF.getData()
        
    #SPECIFIC; INPUT date and data; UPDATE data into editorFrame
    def fillData(self,actionUnit):
        self.IEF.fillData(actionUnit)

    
    def setTutorialLabels(self):
        #新建页面并且初始化标语
        self.fillData(None)
        
    #TODO
    

        
            
            
        