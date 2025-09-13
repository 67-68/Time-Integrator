from ti.core.eventBus import EventBus
from ti.core.Interfaces.presenter.page_presenter_interface import IPagePresenter
from ti.features.core_capture.CapturePage import New_CapturePage
from ti.model.events import PluginEvents
from ti.model.page_contributions import PageContribution



class CapturePagePresenter(IPagePresenter):
    def __init__(
        self,
        capture_page: New_CapturePage,
        bus: EventBus
    ):
        """
        这个presenter用来管理capturePage
        监听插件生成，检查是否有创建页面的请求
        """
        self._page = capture_page
        self._page_contributions = {}
        self._bus = bus
        
        self.initialize()
    
    @property
    def page(self):
        return self._page
    
    @property
    def page_contributions(self):
        return self._page_contributions
    
    @property
    def bus(self):
        return self._bus
    
    def initialize(self):
        """
        初始化方法
        """
        self.bus.subscribe(PluginEvents.PAGE_PLUGIN_CREATED.value,self._on_page_needed)
        self.page.page_first_clicked.connect(self._on_page_first_clicked)
    
    def _on_page_needed(self, page_contributions: list[PageContribution]):
        for contribution in page_contributions:
            print(f"examine page contribution {contribution.page_id}")
            if contribution.parent_page == self.page.page_name:
                page_id = contribution.page_id
                self.page_contributions[page_id] = contribution

                # 应用page_contribution
                self.create_page_contribution(contribution)
    
