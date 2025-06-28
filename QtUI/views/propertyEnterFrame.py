from QtUI.views.rawUI.ui_rawPropertyEnterFrame import Ui_propertyEnterFrame
from PyQt6.QtWidgets import QFrame

class PropertyEnterFrame(QFrame):
    def __init__(self, parent = None):
        super().__init__(parent)
    
        self.editorFrame = Ui_propertyEnterFrame()
        self.editorFrame.setupUi(self)