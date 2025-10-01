from PyQt6.QtWidgets import QCalendarWidget
from PyQt6.QtCore import pyqtSignal, QDate


class Calendar(QCalendarWidget):
    date_selected = pyqtSignal(str)  # 信号：日期被选择，传递日期字符串
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        """设置UI样式"""
        self.setGridVisible(True)
        self.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
    
    def connect_signals(self):
        """连接信号"""
        self.selectionChanged.connect(self._on_date_selected)
    
    def _on_date_selected(self):
        """处理日期选择事件"""
        selected_date = self.selectedDate()
        date_str = selected_date.toString("yyyy-MM-dd")
        self.date_selected.emit(date_str)
    