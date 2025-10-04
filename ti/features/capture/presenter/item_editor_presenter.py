from typing import Any
from ti.features.capture.view.smart_input import SmartInputView
from ti.features.capture.model.ButtonGroup import ButtonGroup
from ti.features.capture.presenter.item_editor_presenter_interface import IItemEditorPresenter
from ti.features.capture.view.input_view import CAP_InputView
from ti.features.capture.view.property import PropertyView
from ti.features.translation.service.translator_service import Translator
from PyQt6.QtCore import QSignalBlocker,pyqtSignal

from ti.model.action_unit import ActionUnit

class ActionUnitEditorPresenter(IItemEditorPresenter):
    save_data = pyqtSignal(Any)
    
    def __init__(
        self,
        translator: Translator,
        parent=None
    ):
        
        super().__init__(parent)
        # 创建主视图
        self.input_view = CAP_InputView()
        
        # 创建子组件
        self.smart_input_view = SmartInputView()
        self.property_view = PropertyView()
        
        # 将子组件添加到主视图
        self.input_view.add_smart_input(self.smart_input_view)
        self.input_view.add_property(self.property_view)
        
        # 创建按钮组并添加到底部
        self.button_group = ButtonGroup()
        self.input_view.add_to_bottom_widget(self.button_group)
        
        self.translator = translator
        
        
    def initialize(self):
        """初始化presenter"""
        # 设置信号连接
        self._setup_signal_connections()
    
    @property
    def view(self):
        """获取主视图widget"""
        return self.input_view
    
    def _setup_signal_connections(self):
        """设置信号连接"""
        # 连接智能输入文本变化信号
        self.smart_input_view.connect_text_changed(self._on_smart_input_changed)
        
        # 连接属性变化信号
        self.property_view.connect_property_changed(self._on_property_changed)
        
        # 连接按钮组信号
        self.button_group.save_requested.connect(self._on_save_data)
        # self.button_group.new_requested.connect(self._on_new_requested) #没想好New和Delete要不要放进核心逻辑，怎么处理
        # self.button_group.delete_requested.connect(self._on_delete_requested)
    
    def fill_data(self,unit: ActionUnit):
        self.unit = unit
        self.property_view.set_property_data(unit)
        
    def _on_smart_input_changed(self, text):
        """处理智能输入文本变化"""
        # 使用信号阻塞器避免循环更新
        with QSignalBlocker(self.property_view):
            # 将智能输入文本翻译为属性数据并设置到属性视图
            property_data = self.translator.trans_other(text)
            if property_data:
                self.property_view.set_property_data(property_data)
                
            
    def collect_and_assign_unit(self):
        data = self.property_view.get_property_data()
        self.unit.action = data["action"]
        self.unit.action_detail = data["action_detail"]
        self.unit.action_type = data["action_type"]
        self.unit.start = data["start"]
        self.unit.end = data["end"]
    
    def _on_property_changed(self, property_data):
        """处理属性变化"""
        # 使用信号阻塞器避免循环更新
        with QSignalBlocker(self.smart_input_view):
            # 将属性数据翻译为智能输入文本并设置到智能输入视图
            fast_entry_text = self.translator.trans_au(property_data)
            if fast_entry_text:
                self.smart_input_view.set_text(fast_entry_text)

    def _on_save_data(self):
        """处理保存请求"""
        self.save_data.emit(self.unit)
        
        
    @property
    def name(self):
        return "action_unit_editor"
    
    @property
    def view(self):
        return self.input_view
    
    def shutdown(self):
        return super().shutdown()