from ti.features.capture_test.model.protocols.selection_protocol import SelectionProtocol
from ti.model.plugin.page_extension_interface import IPageExtension
from ti.features.capture.presenter.selection_presenter import CAP_SelectionPresenter
from ti.features.capture.presenter.input_presenter import CAP_InputPresenter
from ti.features.capture.view.capture import CaptureView
from ti.features.translation.service.translator_service import Translator
from ti.model.core_pages import CoreView
from ti.model.plugin.page_contributions import PageContribution
from ti.model.strategy.strategy_contribution import StrategyContribution
from ti.model.strategy.strategy_needed_decorator import strategy_needed
from ti.model.strategy.strategy_provider_interface import IStrategyProvider
from ti.services.dataService import DataService
from ti.features.capture.presenter.capture_presenter import CapturePresenter
from ti.core.eventBus import EventBus
from ti.view.BasicFrame import BasicFrame



class TESTCapturePlugin(IPageExtension,IStrategyProvider):
    def __init__(
        self,
        data_service: DataService,
        translator: Translator
    ):
        super().__init__()
        self.data_service = data_service
        self.event_bus = None
        self.presenter = None
        self.translator = translator
        
    
    @property
    def strategy_contribution(self):
        return StrategyContribution("test",TestStrategy)
    
    def initialize(self, eventBus: EventBus):
        """初始化插件"""
        self.event_bus = eventBus
        
        # 发布插件注册事件
        self.event_bus.publish("PagePluginRegistered", self.page_contributions)

    @property
    def name(self):
        return "capture_plugin_test"
    
    def shutdown(self):
        """关闭插件"""
        if self.presenter:
            self.presenter.shutdown()
            self.presenter = None
    
    @property
    def page_contributions(self):
        parent_page = CoreView.CAPTURE_PAGE.value
        page_id = "capture_plugin_page_test"
        navigation_name = "输入行动_test"
        
        capture_plugin_page = PageContribution(
            page_id,
            navigation_name,
            parent_page,
            create_page_callback=self.create_page
        )
        
        page_contributions = [capture_plugin_page]
        
        return page_contributions
        
    def create_page(self, page_id):
        """创建指定页面"""
        if page_id == "capture_plugin_page_test":
            return self.create_capture_view()
        
        return None
    
    def create_capture_view(self) -> CaptureView:
        # 创建presenter，它会自动创建widget
        
        selection = self.create_selection()
        
        input = CAP_InputPresenter(self.translator)
        
        presenter = CapturePresenter(
            self.data_service,
            self.event_bus,
            selection,
            input
        )
        
        # 存储presenter引用以便后续管理
        self.presenter = presenter
        
        # 返回presenter创建的widget
        return presenter.widget


    @strategy_needed(SelectionProtocol)
    def create_selection(self,strategy = None):
        if strategy:
            view = strategy.create_selection_view()
        else:
            view = CAP_SelectionPresenter()
    
        return view
    
    
"""需要定义：
一个接受strategy的函数
一个@runtimecheckable的protocol
一个Strategy"""


class TestStrategy:
    def __init__(self):
        pass
    def create_selection_view(self) -> BasicFrame:
        return BasicFrame()