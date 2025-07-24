from PyQt6.QtWidgets import QFrame

from ti.utils import apply_shadow


class BasicFrame(QFrame):
    def __init__(self, parent = None):
        super().__init__(parent)
        
        apply_shadow(self)