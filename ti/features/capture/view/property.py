from PyQt6.QtWidgets import QHBoxLayout, QFormLayout, QFrame, QLabel, QLineEdit, QCheckBox
from ti.view.widgets.other.RealTimeSearchEdit import RealTimeSearchEdit
from ti.view.widgets.pages.BasicWidget import BasicWidget


class PropertyView(BasicWidget):
    """属性视图 - 基于PropertyEnterFrame模板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI布局"""
        # 创建主布局
        main_layout = QHBoxLayout(self)
        
        # 左侧属性面板
        self.left_frame = self._create_left_property_frame()
        main_layout.addWidget(self.left_frame)
        
        # 右侧属性面板
        self.right_frame = self._create_right_property_frame()
        main_layout.addWidget(self.right_frame)
        
        self.setLayout(main_layout)
    
    def _create_left_property_frame(self):
        """创建左侧属性面板"""
        frame = QFrame(self)
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setFrameShadow(QFrame.Shadow.Raised)
        
        layout = QFormLayout(frame)
        
        # 开始时间
        self.start_label = QLabel("开始时间", frame)
        self.start_edit = QLineEdit(frame)
        self.start_edit.setMinimumSize(100, 0)
        layout.addRow(self.start_label, self.start_edit)
        
        # 结束时间
        self.end_label = QLabel("结束时间", frame)
        self.end_edit = QLineEdit(frame)
        layout.addRow(self.end_label, self.end_edit)
        
        # 行动类型
        self.action_type_label = QLabel("行动类型", frame)
        self.action_type_edit = QLineEdit(frame)
        layout.addRow(self.action_type_label, self.action_type_edit)
        
        # 行动内容
        self.action_label = QLabel("行动内容", frame)
        self.action_edit = RealTimeSearchEdit(frame)
        layout.addRow(self.action_label, self.action_edit)
        
        return frame
    
    def _create_right_property_frame(self):
        """创建右侧属性面板"""
        frame = QFrame(self)
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setFrameShadow(QFrame.Shadow.Raised)
        
        layout = QFormLayout(frame)
        
        # 行动详情
        self.action_detail_label = QLabel("行动详情", frame)
        self.action_detail_edit = QLineEdit(frame)
        layout.addRow(self.action_detail_label, self.action_detail_edit)
        
        # 紧急程度
        self.urgency_checkbox = QCheckBox("紧急", frame)
        layout.addRow(self.urgency_checkbox)
        
        # 重要程度
        self.importance_checkbox = QCheckBox("重要", frame)
        layout.addRow(self.importance_checkbox)
        
        return frame
    
    def get_property_data(self):
        """获取所有属性数据"""
        return {
            'start_time': self.start_edit.text(),
            'end_time': self.end_edit.text(),
            'action_type': self.action_type_edit.text(),
            'action': self.action_edit.text(),
            'action_detail': self.action_detail_edit.text(),
            'is_urgent': self.urgency_checkbox.isChecked(),
            'is_important': self.importance_checkbox.isChecked()
        }
    
    def set_property_data(self, data):
        """设置属性数据"""
        if 'start_time' in data:
            self.start_edit.setText(data['start_time'])
        if 'end_time' in data:
            self.end_edit.setText(data['end_time'])
        if 'action_type' in data:
            self.action_type_edit.setText(data['action_type'])
        if 'action' in data:
            self.action_edit.setText(data['action'])
        if 'action_detail' in data:
            self.action_detail_edit.setText(data['action_detail'])
        if 'is_urgent' in data:
            self.urgency_checkbox.setChecked(data['is_urgent'])
        if 'is_important' in data:
            self.importance_checkbox.setChecked(data['is_important'])
    
    def clear_properties(self):
        """清空所有属性"""
        self.start_edit.clear()
        self.end_edit.clear()
        self.action_type_edit.clear()
        self.action_edit.clear()
        self.action_detail_edit.clear()
        self.urgency_checkbox.setChecked(False)
        self.importance_checkbox.setChecked(False)