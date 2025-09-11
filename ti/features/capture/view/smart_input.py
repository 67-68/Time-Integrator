from PyQt6.QtWidgets import QHBoxLayout, QLabel
from ti.view.widgets.other.RealTimeSearchEdit import RealTimeSearchEdit
from ti.view.widgets.pages.BasicWidget import BasicWidget


class SmartInputView(BasicWidget):
    """智能输入视图 - 基于FastEntry模板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI布局"""
        # 创建主布局
        layout = QHBoxLayout(self)
        
        # 创建标签
        self.fast_entry_label = QLabel("快速输入", self)
        layout.addWidget(self.fast_entry_label)
        
        # 创建实时搜索输入框
        self.fast_entry = RealTimeSearchEdit(self)
        layout.addWidget(self.fast_entry)
        
        self.setLayout(layout)
    
    def get_text(self):
        """获取输入文本"""
        return self.fast_entry.text()
    
    def set_text(self, text):
        """设置输入文本"""
        self.fast_entry.setText(text)
    
    def clear_text(self):
        """清空输入文本"""
        self.fast_entry.clear()