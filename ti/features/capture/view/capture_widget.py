from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSplitter
from PyQt6.QtCore import Qt, pyqtSignal

from ti.features.capture.view.dateSelectionFrame import DateSelectionFrame
from ti.features.capture.view.inputEnterFrame import InputEnterFrame
from ti.features.capture.view.editorFrame import EditorFrame
from ti.features.capture.view.bulkEnterFrame import BulkEnterFrame
from ti.model.action_unit import ActionUnit


class CaptureWidget(QWidget):
    """
    CaptureWidget是capture插件的主要UI组件
    整合日历、记录选择、智能输入等子功能
    """
    
    # 信号定义
    actionUnitCreated = pyqtSignal(ActionUnit)
    actionUnitSelected = pyqtSignal(ActionUnit) 
    dateChanged = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.connect_signals()
        
        # 当前状态
        self.current_action_unit = None
        self.current_date = None
        
    def setup_ui(self):
        """设置UI布局"""
        main_layout = QHBoxLayout(self)
        
        # 创建主分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左侧：日历和记录选择
        self.date_selection_frame = DateSelectionFrame()
        splitter.addWidget(self.date_selection_frame)
        
        # 右侧：输入区域
        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)
        
        # 智能输入框
        self.input_enter_frame = InputEnterFrame()
        input_layout.addWidget(self.input_enter_frame)
        
        # 编辑器（可能需要切换显示）
        self.editor_frame = EditorFrame()
        input_layout.addWidget(self.editor_frame)
        
        # 批量输入框
        self.bulk_enter_frame = BulkEnterFrame()
        input_layout.addWidget(self.bulk_enter_frame)
        
        splitter.addWidget(input_widget)
        
        # 设置分割器比例
        splitter.setSizes([300, 700])
        
        main_layout.addWidget(splitter)
        
    def connect_signals(self):
        """连接信号"""
        # 日期选择信号
        self.date_selection_frame.dateSelected.connect(self._on_date_selected)
        self.date_selection_frame.list_item_selected.connect(self._on_action_unit_selected)
        
        # 输入框信号
        self.input_enter_frame.finalDataSubmitted.connect(self._on_final_data_submitted)
        self.editor_frame.saveData_button_clicked.connect(self._on_editor_save)
        self.bulk_enter_frame.saveData_button_clicked.connect(self._on_bulk_save)
        
    def _on_date_selected(self, date_str: str):
        """处理日期选择事件"""
        self.current_date = date_str
        self.dateChanged.emit(date_str)
        
    def _on_action_unit_selected(self, action_unit: ActionUnit):
        """处理ActionUnit选择事件"""
        self.current_action_unit = action_unit
        self.actionUnitSelected.emit(action_unit)
        
        # 同步数据到编辑器
        if hasattr(self.editor_frame, 'fillData'):
            self.editor_frame.fillData(action_unit)
            
    def _on_final_data_submitted(self, data: dict):
        """处理智能输入提交事件"""
        # 创建新的ActionUnit
        action_unit = ActionUnit(
            start=data.get("start", ""),
            end=data.get("end", ""),
            action=data.get("action", ""),
            action_detail=data.get("action_detail", ""),
            action_type=data.get("action_type", ""),
            timeSpan=data.get("timeSpan", 0)
        )
        
        self.current_action_unit = action_unit
        self.actionUnitCreated.emit(action_unit)
        
    def _on_editor_save(self, data: dict):
        """处理编辑器保存事件"""
        if self.current_action_unit:
            # 更新当前ActionUnit
            self.current_action_unit.start = data.get("start", "")
            self.current_action_unit.end = data.get("end", "")
            self.current_action_unit.action = data.get("action", "")
            self.current_action_unit.action_detail = data.get("action_detail", "")
            self.current_action_unit.action_type = data.get("action_type", "")
            self.current_action_unit.timeSpan = data.get("timeSpan", 0)
            
            self.actionUnitCreated.emit(self.current_action_unit)
            
    def _on_bulk_save(self, data: dict):
        """处理批量输入保存事件"""
        # 批量输入可能创建多个ActionUnit
        # 这里需要根据具体的批量输入格式来处理
        if isinstance(data, list):
            for item in data:
                action_unit = ActionUnit(
                    start=item.get("start", ""),
                    end=item.get("end", ""),
                    action=item.get("action", ""),
                    action_detail=item.get("action_detail", ""),
                    action_type=item.get("action_type", ""),
                    timeSpan=item.get("timeSpan", 0)
                )
                self.actionUnitCreated.emit(action_unit)
        else:
            action_unit = ActionUnit(
                start=data.get("start", ""),
                end=data.get("end", ""),
                action=data.get("action", ""),
                action_detail=data.get("action_detail", ""),
                action_type=data.get("action_type", ""),
                timeSpan=data.get("timeSpan", 0)
            )
            self.actionUnitCreated.emit(action_unit)
            
    def fill_date_data(self, date_data: list):
        """填充日期数据到日历组件"""
        if hasattr(self.date_selection_frame, 'fillData'):
            self.date_selection_frame.fillData(date_data)
            
    def set_current_date(self, date_str: str):
        """设置当前日期"""
        self.current_date = date_str
        # 可以触发日历组件更新
        
    def get_current_action_unit(self) -> ActionUnit:
        """获取当前选中的ActionUnit"""
        return self.current_action_unit