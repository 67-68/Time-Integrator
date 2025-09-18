from ti.core.Interfaces.presenter.page_presenter_interface import IPagePresenter
from ti.core.Interfaces.view.page_view_interface import IPageView
from ti.core.eventBus import EventBus


class PagePresenter(IPagePresenter):
    def __init__(
        self,
        bus: EventBus,
        page: type[IPageView]
    ):
        super().__init__()
        self.bus = bus
        self.page = page
        self.page_contributions = {}
        
    def initialize(self):
        return super().initialize()
    
    def _on_page_first_clicked(self, page_id):
        return super()._on_page_first_clicked(page_id)
    
    def _on_page_needed(self, page_contributions):
        return super()._on_page_needed(page_contributions)
    
    def create_page_contribution(self, contribution):
        return super().create_page_contribution(contribution)
    
    def create_button(self, contribution):
        return super().create_button(contribution)