from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QListWidget


class RecordList(QListWidget):
    # 信号：记录项被点击，传递ActionUnit对象
    record_clicked = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        """设置UI样式"""
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
    
    def get_selected_action_unit(self):
        """
        获取当前选中的ActionUnit对象
        :return: 选中的ActionUnit对象，如果没有选中则返回None
        """
        current_item = self.currentItem()
        if current_item:
            # 从UserRole(1000)获取存储的ActionUnit对象
            action_unit = current_item.data(1000)
            return action_unit
        return None
    
    def connect_signals(self):
        """连接信号"""
        self.itemClicked.connect(self._on_item_clicked)

    def _on_item_clicked(self, item):
        """处理项目点击事件"""
        # 获取选中的ActionUnit对象
        action_unit = self.get_selected_action_unit()
        if action_unit:
            # 发射信号传递ActionUnit对象
            self.record_clicked.emit(action_unit)
        