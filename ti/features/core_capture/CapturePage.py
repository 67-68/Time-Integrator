
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget
from ti.core.Interfaces.view.page_view_interface import IPageView
from ti.model.core_pages import CoreView
from ti.view.rawUI.ui_rawNewCapturePage import Ui_NewCapturePage


class New_CapturePage(QWidget, IPageView):
    
    page_first_clicked = pyqtSignal(str)
    
    def __init__(
        self,
        parent = None
    ):
        super().__init__(parent)
        self.initialize()
    
    def initialize(self):
        self.page = Ui_NewCapturePage()
        self.page.setupUi(self)
        
        # 删除默认的pages
        while self.page.stackedWidget.count() > 0:
            widget = self.page.stackedWidget.widget(0)
            self.page.stackedWidget.removeWidget(widget)
            
        self.pages = {}
    
    @property
    def page_name(self) -> str:
        """
        返回页面名称
        """
        return CoreView.CAPTURE_PAGE.value
            
    def create_navigation_btn(self, btn_data):
        return super().create_navigation_btn(btn_data)
    
    def _on_navigation_btn_clicked(self, page_id):
        return super()._on_navigation_btn_clicked(page_id)
    
    def add_page_to_stack(self, page_id, page_widget):
        return super().add_page_to_stack(page_id, page_widget)
    
    def switch_to_page(self, page_id):
        return super().switch_to_page(page_id)