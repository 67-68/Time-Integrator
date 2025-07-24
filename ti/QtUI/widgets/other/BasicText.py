from PyQt6.QtWidgets import QTextEdit
class BasicText(QTextEdit):
    def __init__(self, master,**kwargs):
        super().__init__(master,**kwargs)
        self.setReadOnly(True)
        self.setMinimumHeight(10)
        self.setMinimumWidth(40)
    
    def setText(self, text):
        self.setReadOnly(False)
        self.setPlainText(text)   # 或 setHtml(text) 支持富文本
        self.setReadOnly(True)