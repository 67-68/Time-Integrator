
from PyQt6.QtCore import pyqtSignal
from ti.core.Interfaces.view.page_view_interface import IPageView




class New_CapturePage(IPageView):
    
    page_first_clicked = pyqtSignal(str)
    
    def __init__(
        self,
        parent = None
    ):
        super().__init__(parent)
        self.initialize()
    
    def initialize(self):
        return super().initialize()
    
    @property
    def page_name(self) -> str:
        """
        返回页面名称
        """
        return "capture"
            
    def create_navigation_btn(self, btn_data):
        return super().create_navigation_btn(btn_data)
    
    def _on_navigation_btn_clicked(self, page_id):
        return super()._on_navigation_btn_clicked(page_id)
    
    def add_page_to_stack(self, page_id, page_widget):
        return super().add_page_to_stack(page_id, page_widget)
    
    def switch_to_page(self, page_id):
        return super().switch_to_page(page_id)