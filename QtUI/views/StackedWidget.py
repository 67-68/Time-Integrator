from PyQt6.QtWidgets import QStackedWidget

class StackedWidget(QStackedWidget):
    def __init__(self, master, **kwargs):
        super().__init__(master,**kwargs)
        