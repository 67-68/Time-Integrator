from PyQt6.QtWidgets import QLabel

class BasicLabel(QLabel):
    def __init__(self, master,text,**kwargs):
        super().__init__(master,text = text,**kwargs)
        text = text