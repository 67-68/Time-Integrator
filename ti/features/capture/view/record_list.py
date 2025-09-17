from PyQt6.QtWidgets import QListWidget


class RecordList(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
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
        