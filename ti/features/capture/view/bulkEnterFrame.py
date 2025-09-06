
from PyQt6.QtCore import pyqtSignal

from ti.presenters.inputValidationPresentor import InputValidation

from ti.services.analysis.matchers import get_time_from_str
from ti.services.translator import Translator
from ti.view.rawUI.ui_rawBulkEnterFrame import Ui_bulkEnterFrame
from ti.view.widgets.pages.BasicWidget import BasicWidget




class BulkEnterFrame(BasicWidget):
    saveData_button_clicked = pyqtSignal(dict)
    
    def __init__(self, parent = None):
        super().__init__(parent)

        self.BEF = Ui_bulkEnterFrame()
        self.BEF.setupUi(self)
        
        self.BE = self.BEF.bulkTextEdit
        self.SB = self.BEF.submitButton
        self.trans = Translator()
        self.vali = InputValidation()
        
        #  --- 信号 ---
        self.SB.clicked.connect(self._on_button_clicked)
        
    #  ------ 提交功能 ------
    def _on_button_clicked(self):
        text = self.BE.toPlainText() #TODO
        actionUnits = text.split("\n")
        for au in actionUnits:
            advice = self.trans.fastToProper(au)
            property = advice["data"]
            property["timeSpan"] = get_time_from_str(property["end"]) - get_time_from_str(property["start"])
            
            validity = self.vali.validation(property,"actionUnit")
            if validity != True:
                print (validity)
                return
            
            self.saveData_button_clicked.emit(property)
    
    def fillData(self,data):
        """
        this function is used to fill data when date is selected
        it will take in the action units of that day, translate them into fast entry, then present them
        """
        
        text = ""
        if data:
            for au in data:
                fastEntry = self.trans.properToFast(au)
                text = text + fastEntry + "\n"
            
            self.BE.setText(text)
            