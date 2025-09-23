from ti.model.plugin.page_extension_interface import IPageExtension
from ti.model.core_pages import CoreView
from ti.model.plugin.page_contributions import PageContribution



class DocumentPlugin(
    IPageExtension
):
    def __init__(self):
        super().__init__()
        
    def initialize(self, eventBus):
        return super().initialize(eventBus)
    
    
    def shutdown(self):
        return super().shutdown()
    
    @property
    def name(self):
        return "document"
    
    def create_page(self):
        return super().create_page()
    
    @property
    def page_contributions(self):
        parent_page = CoreView.CAPTURE_PAGE.value
        page_id = "document_page"
        navigation_name = "查看数据库"
        
        capture_plugin_page = PageContribution(
            page_id,
            navigation_name,
            parent_page,
            create_page_callback=self.create_page
        )
        
        return capture_plugin_page
    