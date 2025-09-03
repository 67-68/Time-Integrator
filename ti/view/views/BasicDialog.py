from PyQt6.QtWidgets import QDialog

from ti.view.rawUI.ui_rawDialog import Ui_Dialog

class BasicDialog(QDialog):
    def __init__(self,ui,parent = None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        self.ui.dialogLayout.addWidget(ui)
    