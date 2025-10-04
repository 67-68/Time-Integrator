from PyQt6.QtWidgets import QWidget

from ti.services.utils import apply_shadow


class BasicWidget(QWidget):
    def __init__(self, parent = None, **kwargs):
        super().__init__(parent,**kwargs)
        
        apply_shadow(self)
        