from PyQt6.QtWidgets import QWidget

class CenterMainFrame(QWidget):
    def __init__(self, fatherFrame = None):
        super().__init__(fatherFrame)
        self.setStyleSheet("background-color:#F4F4F4;")
