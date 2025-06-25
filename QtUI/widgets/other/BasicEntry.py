from PyQt6.QtWidgets import QLineEdit

class BasicEntry(QLineEdit):
    def __init__(self, master,**kwargs):
        super().__init__(master,**kwargs)
        self.setFixedWidth(20)
    
    def setEntry(self,text):
        self.clear()
        self.insert(0,text)