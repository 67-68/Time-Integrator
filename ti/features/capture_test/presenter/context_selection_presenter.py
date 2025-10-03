import datetime
from ti.features.capture_test.presenter.context_selection_presenter_interface import IContextSelectionPresenter
from ti.features.capture.view.calendar import Calendar
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy

from ti.features.capture_test.model.selection_condition import SelectionCondition


class ContextSelectionPresenter(IContextSelectionPresenter):
    selection_condition_changed = pyqtSignal(SelectionCondition)

    def __init__(self):
        super().__init__()
        # 创建QWidget容器来包装Calendar，避免类型不匹配
        self._container = QWidget()
        self._container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._container.setMinimumSize(200, 150)

        # 设置布局，确保Calendar充满整个容器
        layout = QVBoxLayout(self._container)
        layout.setContentsMargins(0, 0, 0, 0)  # 移除边距，让Calendar紧贴边界
        layout.setSpacing(0)  # 移除间距

        # 创建Calendar作为容器的子组件
        self._calendar = Calendar(self._container)
        self._calendar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self._calendar)

        # 连接信号
        self._calendar.selectionChanged.connect(self._on_selection_condition_change)
        
    def _on_selection_condition_change(self):
        selected_date = self._calendar.selectedDate()
        date_str = selected_date.toString("yyyy-MM-dd")
        self.selection_condition_changed.emit(SelectionCondition("action_unit",date=date_str))
    
    @property
    def view(self):
        return self._container

    def initialize(self):
        return super().initialize()

    def shutdown(self):
        return super().shutdown()

    @property
    def name(self):
        return "calandar_context_selection_presenter"

    def get_selection_condition(self):
        """获取当前选择的日期"""
        selected_date = self._calendar.selectedDate()
        date_str = selected_date.toString("yyyy-MM-dd")
        return SelectionCondition("action_unit",date=date_str)