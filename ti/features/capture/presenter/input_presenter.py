from ti.features.translation.service.translator_service import Translator
from ti.presenters.BasePresenter import BasePresenter
from ti.features.capture.view.input_view import CAP_InputView
from ti.features.capture.view.smart_input import SmartInputView
from ti.features.capture.view.property import PropertyView
from ti.services.synthesizer_service import Synthesizer
from ti.features.capture.model.ButtonGroup import ButtonGroup
from PyQt6.QtCore import QSignalBlocker, pyqtSignal,QObject


class CAP_InputPresenter(QObject):
    # 信号定义
    save_requested = pyqtSignal(dict)
    new_requested = pyqtSignal()
    delete_requested = pyqtSignal(dict)
    
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
    
    def get_widget(self):
        """获取主视图widget"""
        return self.input_view
    
    def _setup_signal_connections(self):
        """设置信号连接"""
        # 连接智能输入文本变化信号
        self.smart_input_view.connect_text_changed(self._on_smart_input_changed)
        
        # 连接属性变化信号
        self.property_view.connect_property_changed(self._on_property_changed)
        
        # 连接按钮组信号
        self.button_group.save_requested.connect(self._on_save_requested)
        self.button_group.new_requested.connect(self._on_new_requested)
        self.button_group.delete_requested.connect(self._on_delete_requested)
    
    def _on_smart_input_changed(self, text):
        """处理智能输入文本变化"""
        # 使用信号阻塞器避免循环更新
        with QSignalBlocker(self.property_view):
            # 将智能输入文本翻译为属性数据并设置到属性视图
            property_data = self.translator.trans_other(text)
            if property_data:
                self.property_view.set_property_data(property_data)
    
    def _on_property_changed(self, property_data):
        """处理属性变化"""
        # 使用信号阻塞器避免循环更新
        with QSignalBlocker(self.smart_input_view):
            # 将属性数据翻译为智能输入文本并设置到智能输入视图
            fast_entry_text = self.translator.trans_au(property_data)
            if fast_entry_text:
                self.smart_input_view.set_text(fast_entry_text)
    
    def _on_save_requested(self):
        """处理保存请求"""
        # 从属性视图获取数据
        property_data = self.property_view.get_property_data()
        # 发射信号到capture presenter
        self.save_requested.emit(property_data)
    
    def _on_new_requested(self):
        """处理新建请求"""
        # 发射信号到capture presenter
        self.new_requested.emit()
    
    def _on_delete_requested(self):
        """处理删除请求"""
        # 从属性视图获取当前数据用于删除
        property_data = self.property_view.get_property_data()
        # 发射信号到capture presenter
        self.delete_requested.emit(property_data)