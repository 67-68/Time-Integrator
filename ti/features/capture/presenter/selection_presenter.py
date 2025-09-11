from PyQt6.QtCore import QObject
from ti.features.capture.view.selection_view import SelectionView


class CAP_SelectionPresenter(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.view = SelectionView()
        self.connect_signals()
    
    def connect_signals(self):
        """连接信号"""
        # 连接日历的日期选择信号
        self.view.calendar.date_selected.connect(self._on_date_selected)
    
    def _on_date_selected(self, date_str):
        """处理日期选择事件"""
        print(f"Date selected: {date_str}")
        # 这里可以添加处理日期选择的逻辑，比如加载该日期的记录