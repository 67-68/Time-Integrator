from QtUI.views.rawUI.ui_rawFastEntry import Ui_rawFastEnterFrame
from PyQt6.QtWidgets import QFrame

class fastEnterFrame(QFrame):
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.fastEnterFrame = Ui_rawFastEnterFrame()
        self.fastEnterFrame.setupUi(self)