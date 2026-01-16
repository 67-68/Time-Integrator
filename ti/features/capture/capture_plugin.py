from typing import Callable
from ti.features.capture.model.protocols.renderable_item_protocol import IRenderableItemProtocol
from ti.features.capture.model.protocols.view_protocol import ICaptureView, IContextSelection, IItemDisplay, IItemEditor
from ti.features.capture.presenter.capture_presenter import CapturePresenter
from ti.features.capture.presenter.context_selection_presenter import ContextSelectionPresenter
from ti.features.capture.presenter.list_display_presenter import ListDisplayPresenter
from ti.features.capture.presenter.item_editor_presenter import ActionUnitEditorPresenter
from ti.model.plugin.page_extension_interface import IPageExtension
from ti.features.capture.view.capture_view import CaptureView
from ti.features.translation.service.translator_service import Translator
from ti.model.core_pages import CoreView
from ti.model.plugin.page_contributions import PageContribution
from ti.services.dataService import DataService
from ti.core.eventBus import EventBus
from ti.services.strategy_service import StrategyService



class CapturePlugin(IPageExtension):
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
        # 他们应该是list(presenter)
        # 获取所有可能的View
        context_selection_presenters = StrategyService.execute_strategies_from_protocol(IContextSelection)
        item_editor_presenters = StrategyService.execute_strategies_from_protocol(IItemEditor)
        item_display_presenters = StrategyService.execute_strategies_from_protocol(IItemDisplay)

        # 加入默认View
        context_selection_presenters.append(ContextSelectionPresenter())
        item_display_presenters.append(ListDisplayPresenter())
        item_editor_presenters.append(ActionUnitEditorPresenter(self.translator))
        
        data_models = StrategyService.execute_strategies_from_protocol(IRenderableItemProtocol)

        presenter =StrategyService.execute_with_strategy(
            ICaptureView,
            CapturePresenter,
            self.data_service,
            self.event_bus,
            context_selection_presenters,
            item_display_presenters,
            item_editor_presenters,
            data_models
        )
        
        # 存储presenter引用以便后续管理
        self.presenter = presenter
        
        # 返回presenter创建的widget
        return presenter.view
    
    

    
    
"""
需要定义：
一个接受strategy的函数
一个@runtimecheckable的protocol
一个Strategy
"""