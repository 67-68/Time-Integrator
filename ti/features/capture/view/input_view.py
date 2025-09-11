from PyQt6.QtWidgets import QVBoxLayout, QSizePolicy
from ti.view.widgets.pages.BasicWidget import BasicWidget


class CAP_InputView(BasicWidget):
    """
    用来盛装button, PropertyFrame和smartInputFrame
    鉴于它是用来容纳提升物件的类，直接叫view
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.smart_input_view = None
        self.property_view = None
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI布局"""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.setLayout(self.main_layout)
    
    def add_smart_input(self, smart_input_view):
        """添加智能输入视图"""
        self.smart_input_view = smart_input_view
        smart_input_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        smart_input_view.setMinimumSize(200, 100)
        self.main_layout.addWidget(smart_input_view, 1)
    
    def add_property(self, property_view):
        """添加属性视图"""
        self.property_view = property_view
        property_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        property_view.setMinimumSize(200, 200)
        self.main_layout.addWidget(property_view, 2)
    