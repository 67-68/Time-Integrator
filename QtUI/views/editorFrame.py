from QtUI.views.rawUI.ui_rawEditorFrame import Ui_editorFrame
from PyQt6.QtWidgets import QFrame

class EditorFrame(QFrame):
    def __init__(self, parent = None):
        super().__init__(parent)
    
        self.editorFrame = Ui_editorFrame()
        self.editorFrame.setupUi(self)
    