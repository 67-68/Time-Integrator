from PyQt6.QtCore import pyqtSignal
from ti.model.action_unit import ActionUnit
from ti.view.widgets.pages.BasicWidget import BasicWidget


class CaptureView(BasicWidget):
    """
    CaptureWidget是capture插件的主要UI组件
    整合日历、记录选择、智能输入等子功能
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
