from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QSizePolicy
from ti.model.action_unit import ActionUnit
from ti.view.BasicWidget import BasicWidget


class CaptureView(BasicWidget):
    """
    CaptureWidget是capture插件的主要UI组件
    整合日历、记录选择、智能输入等子功能
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI布局"""
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.setLayout(self.main_layout)
    
    def add_selection_view(self, selection_view):
        """添加选择视图到左侧"""
        selection_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.main_layout.addWidget(selection_view, 1)
    
    def add_input_view(self, input_view):
        """添加输入视图到右侧"""
        input_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.main_layout.addWidget(input_view, 1)
