from PyQt6.QtWidgets import QWidget
from Core.utils import apply_shadow

class BasicWidget(QWidget):
    def __init__(self, master = None, **kwargs):
        super().__init__(master,**kwargs)
        
        apply_shadow(self)
        