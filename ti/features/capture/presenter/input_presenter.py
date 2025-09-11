from ti.presenters.BasePresenter import BasePresenter
from ti.features.capture.view.input_view import CAP_InputView
from ti.features.capture.view.smart_input import SmartInputView
from ti.features.capture.view.property import PropertyView


class CAP_InputPresenter(BasePresenter):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 创建主视图
        self.input_view = CAP_InputView()
        
        # 创建子组件
        self.smart_input_view = SmartInputView()
        self.property_view = PropertyView()
        
        # 将子组件添加到主视图
        self.input_view.add_smart_input(self.smart_input_view)
        self.input_view.add_property(self.property_view)
    
    def initialize(self):
        """初始化presenter"""
        # 这里可以添加初始化逻辑
        return super().initialize()
    
    def shutdown(self):
        """关闭presenter"""
        # 这里可以添加清理逻辑
        return super().shutdown()
    
    def get_widget(self):
        """获取主视图widget"""
        return self.input_view