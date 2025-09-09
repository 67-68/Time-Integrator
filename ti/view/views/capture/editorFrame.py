
from PyQt6.QtCore import pyqtSignal


from ti.presenters.inputValidationPresentor import InputValidation
from ti.features.detector.matchers import get_time_from_str
from ti.view.rawUI.ui_rawEditorFrame import Ui_editorFrame
from ti.view.widgets.pages.BasicWidget import BasicWidget



class EditorFrame(BasicWidget):    
    
    saveData_button_clicked = pyqtSignal(dict)
    actionUnitSelected = pyqtSignal(int)
    new_button_selected = pyqtSignal()
    delete_button_clciked = pyqtSignal(dict)
    
    def __init__(self, parent = None):
        super().__init__(parent)
    
        self.editorFrame = Ui_editorFrame()
        self.editorFrame.setupUi(self)
                
        #  --- 关联回调函数 ---
        self.editorFrame.leftSwitchButton.clicked.connect(lambda: self.actionUnitSelected.emit(-1))
        self.editorFrame.rightSwitchButton.clicked.connect(lambda: self.actionUnitSelected.emit(1))
        self.editorFrame.confirmButton.clicked.connect(self._on_confirmButton_clicked)
        self.editorFrame.createNewButton.clicked.connect(self.new_button_selected.emit)
        #self.editorFrame.deleteButton.clicked.connect()
        
        #  --- 创建检验对象 ---
        self.validation = InputValidation()
        
        #  --- 赋值 ---
        self.EF = self.editorFrame
        self.IEF = self.editorFrame.inputEnterFrameBase

    
    #SPECIFIC; DETECT confirmButton; VALIDATE, COLLECT data and EMIT a signal to presentor
    def _on_confirmButton_clicked(self):
        actionUnits = self.collectData()
        actionUnits["timeSpan"] = get_time_from_str(actionUnits["end"]) - get_time_from_str(actionUnits["start"])
        
        # 把包含 data 键的完整数据包发射出去
        self.saveData_button_clicked.emit(actionUnits)
        
    #SPECIFIC; Collect data from stackedwidget, OUTPUT them as list of actionUnit
    def collectData(self):
        return self.IEF.getData()
        
    #SPECIFIC; INPUT date and data; UPDATE data into editorFrame
    def fillData(self,actionUnit):
        self.IEF.fillData(actionUnit)


    

        
            
            
        