from ti.core.eventBus import EventBus
from ti.core.Interfaces.presenter.page_presenter_interface import IPagePresenter
from ti.features.analysis.analysis_page import AnalysisPage
from ti.model.events import PluginEvents
from ti.model.page_contributions import PageContribution


class AnalysisPagePresenter(IPagePresenter):
    def __init__(
        self,
        analysis_page: AnalysisPage,
        bus: EventBus
    ):
        """
        这个presenter用来管理analysisPage
        监听插件生成，检查是否有创建页面的请求
        """
        self._page = analysis_page
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
        return super().initialize()
    
    def _on_page_first_clicked(self, page_id):
        return super()._on_page_first_clicked(page_id)
