from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from ti.features.capture.view.calendar import Calendar
from ti.features.capture.view.record_list import RecordList


class SelectionView(QWidget):
    # 信号：记录项被点击，传递ActionUnit对象
    record_clicked = pyqtSignal(object)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.calendar = Calendar(self)
        self.calendar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.calendar.setMinimumSize(200, 150)
        
        self.record_list = RecordList(self)
        self.record_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.record_list.setMinimumSize(200, 150)
        
        main_layout.addWidget(self.calendar, 1)
        main_layout.addWidget(self.record_list, 2)
        
        self.setLayout(main_layout)
    
    def connect_signals(self):
        """连接信号"""
        # 连接记录列表的点击事件
        self.record_list.itemClicked.connect(self._on_record_clicked)
    
    def _on_record_clicked(self, item):
        """处理记录项点击事件"""
        # 获取选中的ActionUnit对象
        action_unit = self.record_list.get_selected_action_unit()
        if action_unit:
            # 发射信号传递ActionUnit对象
            self.record_clicked.emit(action_unit)