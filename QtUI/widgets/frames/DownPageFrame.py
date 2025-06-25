from PyQt6.QtWidgets import QWidget,QHBoxLayout
class DownPageFrame(QWidget):
    def __init__(self, master = None):
        super().__init__(master)
        self.setStyleSheet("background-color: #C9B49A;")
    
        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)