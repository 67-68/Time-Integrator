from ti.core.Interfaces.page_extension_interface import PageExtensionInterface
from ti.features.capture.presenter.selection_presenter import CAP_SelectionPresenter
from ti.features.capture.presenter.smart_input_presenter import CAP_InputPresenter
from ti.features.capture.view.capture import CaptureView
from ti.model.page_contributions import PageContribution
from ti.services.dataAccess.dataService import DataService
from ti.features.capture.presenter.capture_presenter import CapturePresenter
from ti.core.eventBus import EventBus


class CapturePlugin(PageExtensionInterface):
    def __init__(
        self,
        data_service: DataService
    ):
        super().__init__()
        self.data_service = data_service
        self.event_bus = None
        self.presenter = None
    
    def initialize(self, eventBus: EventBus):
        """初始化插件"""
        self.event_bus = eventBus
        
        # 发布插件注册事件
        plugin_data = {
            'plugin_name': self.name,
            'page_contributions': self.page_contributions,
            'create_page_callback': self.create_page
        }
        
        self.event_bus.publish("PagePluginRegistered", plugin_data)

    @property
    def name(self):
        return "capture_plugin"
    
    def shutdown(self):
        """关闭插件"""
        if self.presenter:
            self.presenter.shutdown()
            self.presenter = None
    
    @property
    def page_contributions(self):
        parent_page = "CapturePage"
        page_id = "capture_plugin_page"
        navigation_name = "输入行动"
        
        capture_plugin_page = PageContribution(
            page_id,
            navigation_name,
            parent_page
        )
        
        page_contributions = [capture_plugin_page]
        
        return page_contributions
        
    def create_page(self, page_id):
        """创建指定页面"""
        if page_id == "capture_plugin_page":
            return self.create_capture_view()
        
        return None
    
    def create_capture_view(self) -> CaptureView:
        # 创建presenter，它会自动创建widget
        selection = CAP_SelectionPresenter()
        input = CAP_InputPresenter()
        presenter = CapturePresenter(
            self.data_service,
            self.event_bus,
            selection,
            input
        )
