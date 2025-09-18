from ti.core.Interfaces.view.page_view_interface import IPageView
from ti.core.eventBus import EventBus
from PyQt6.QtWidgets import QWidget

class PageView(IPageView,QWidget):
    def __init__(
        self,
        bus: EventBus,
        page_name: str,
        parent = None
    ):
        super().__init__()
        self.initialize()
        self.bus = bus
        self.page_name = page_name
        
    def initialize(self):
        return super().initialize()
        
    def _on_change_page(self, page_name):
        return super()._on_change_page(page_name)
        
    def create_navigation_btn(self, btn_data):
        return super().create_navigation_btn(btn_data)
    
    def _on_navigation_btn_clicked(self, page_id):
        return super()._on_navigation_btn_clicked(page_id)
    
    def add_page_to_stack(self, page_id, page_widget):
        return super().add_page_to_stack(page_id, page_widget)
    
    def switch_to_page(self, page_id):
        return super().switch_to_page(page_id)
    