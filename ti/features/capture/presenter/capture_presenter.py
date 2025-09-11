# 这是插件capture的presenter, 不是capturePage核心的presenter
from PyQt6.QtCore import QObject

from ti.features.capture.presenter.selection_presenter import CAP_SelectionPresenter
from ti.features.capture.presenter.input_presenter import CAP_InputPresenter
from ti.features.capture.view.capture import CaptureView
from ti.services.dataAccess.dataService import DataService
from ti.core.eventBus import EventBus
from ti.model.action_unit import ActionUnit


class CapturePresenter(QObject):
    """
    CapturePresenter管理capture插件的业务逻辑
    协调UI组件和数据服务
    """
    
    def __init__(
        self,
        data_service: DataService,
        event_bus: EventBus,
        selection: CAP_SelectionPresenter,
        input: CAP_InputPresenter
    ):
        super().__init__()
        self.data_service = data_service
        self.event_bus = event_bus
        
        # 管理presenter
        self.selection = selection
        self.input = input
        
        # 创建主视图并设置布局
        self.widget = CaptureView()
        self._setup_view_layout()
        
    def _setup_view_layout(self):
        """设置视图布局 - 左边selection view, 右边input view"""
        # 获取子presenter的view
        selection_view = self.selection.view
        input_view = self.input.get_widget()
        
        # 添加到主视图
        self.widget.add_selection_view(selection_view)
        self.widget.add_input_view(input_view)
        
    def _on_save_btn_pressed(self):
        """
        根据组件传递上来的信号
        首先保存数据
        然后更新展示
        """
        pass
    
        
