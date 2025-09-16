from PyQt6.QtWidgets import QHBoxLayout, QLabel,QLineEdit
from PyQt6.QtCore import pyqtSignal
from ti.view.widgets.other.RealTimeSearchEdit import RealTimeSearchEdit
from ti.view.widgets.pages.BasicWidget import BasicWidget


class SmartInputView(BasicWidget):
    """智能输入视图 - 基于FastEntry模板"""
    
    # 信号定义
    text_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self._setup_signals()
    
    def setup_ui(self):
        """设置UI布局"""
        # 创建主布局
        layout = QHBoxLayout(self)
        
        # 创建标签
        self.fast_entry_label = QLabel("快速输入", self)
        layout.addWidget(self.fast_entry_label)
        
        # 创建实时搜索输入框
        self.fast_entry = QLineEdit(self)
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
    
    def _setup_signals(self):
        """设置信号连接"""
        self.fast_entry.textChanged.connect(self._on_text_changed)
    
    def _on_text_changed(self, text):
        """处理文本变化，发射信号"""
        self.text_changed.emit(text)
    
    def connect_text_changed(self, slot, blocker=None):
        """
        连接文本变化信号到指定槽函数
        :param slot: 槽函数
        :param blocker: 可选的信号阻塞器，用于避免循环更新
        """
        if blocker:
            with blocker:
                self.text_changed.connect(slot)
        else:
            self.text_changed.connect(slot)