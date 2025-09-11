from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from ti.features.capture.view.calendar import Calendar
from ti.features.capture.view.record_list import RecordList


class SelectionView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
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