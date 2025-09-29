"""
Intervention的界面
功能包括
1. 设置一个接下来需要专注的东西
2. 开始时间

接下来在开始时间之后
每分钟插件会提醒一遍电脑
直到用户返回并按下停止按钮（红色）

Its very annoying
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QDateTimeEdit
from PyQt6.QtCore import pyqtSignal, QDateTime
from ti.features.intervention.model.stored.inv_real_time_annoying import RealTimeAnnoying


class InterventionView(QWidget):
    intervention_saved = pyqtSignal(RealTimeAnnoying)
    stop_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Status label at the top
        self.status_label = QLabel("准备设置干预...")
        layout.addWidget(self.status_label)
        
        # Action input
        action_layout = QHBoxLayout()
        action_layout.addWidget(QLabel("行动:"))
        self.action_input = QLineEdit()
        self.action_input.setPlaceholderText("输入你要专注的行动")
        action_layout.addWidget(self.action_input)
        layout.addLayout(action_layout)
        
        # Start time input
        time_layout = QHBoxLayout()
        time_layout.addWidget(QLabel("开始时间:"))
        self.time_input = QDateTimeEdit()
        self.time_input.setDateTime(QDateTime.currentDateTime())
        self.time_input.setCalendarPopup(True)
        time_layout.addWidget(self.time_input)
        layout.addLayout(time_layout)
        
        # Detail input
        detail_layout = QVBoxLayout()
        detail_layout.addWidget(QLabel("详细描述:"))
        self.detail_input = QTextEdit()
        self.detail_input.setPlaceholderText("输入行动的具体描述")
        self.detail_input.setMaximumHeight(100)
        detail_layout.addWidget(self.detail_input)
        layout.addLayout(detail_layout)
        
        # Save button
        self.save_button = QPushButton("保存干预")
        self.save_button.clicked.connect(self.on_save_clicked)
        layout.addWidget(self.save_button)
        
        # Red stop button
        self.stop_button = QPushButton("停止通知")
        self.stop_button.setStyleSheet("background-color: red; color: white;")
        self.stop_button.clicked.connect(self.on_stop_clicked)
        layout.addWidget(self.stop_button)
        
        self.setLayout(layout)
    
    def on_save_clicked(self):
        action_name = self.action_input.text().strip()
        start_time = self.time_input.dateTime().toPyDateTime()
        action_detail = self.detail_input.toPlainText().strip()
        
        if not action_name:
            print("Warning: Action name cannot be empty")
            return
        
        intervention_data = RealTimeAnnoying(
            action_name=action_name,
            action_detail=action_detail,
            start_time=start_time
        )
        
        print(f"Emitting intervention_saved signal with data: {action_name}")
        self.intervention_saved.emit(intervention_data)
        print("Signal emitted successfully")
    
    def on_stop_clicked(self):
        print("Emitting stop_requested signal")
        self.stop_requested.emit()
        print("Stop signal emitted successfully")
    
    def update_status(self, message: str):
        """更新状态标签的内容"""
        self.status_label.setText(message)
