from ti.core.Interfaces.extension_Interface import ExtensionInterface
from ti.core.Interfaces.page_extension_interface import IPageExtension
from ti.core.Interfaces.path_register_provider_interface import IPathRegisterProvider
from ti.features.insight.view.insight_view import InsightView
from ti.model.core_pages import CoreView
from ti.model.page_contributions import PageContribution


class InsightPlugin(
    IPathRegisterProvider,
    IPageExtension
):
    def __init__(self):
        super().__init__()
        
        
    @property
    def page_contributions(self):
        """
        用来存储这个类有什么自定义的界面
        以及它们会被放到哪里

        Returns:
            list[PageContribution]: _description_
        """
        parent_page = CoreView.ANALYSIS_PAGE.value
        page_id = "insight_view"
        navigation_name = "查看洞察"
        
        insight_plugin_page = PageContribution(
            page_id,
            navigation_name,
            parent_page,
            create_page_callback=self.create_page
        )
        
        return [insight_plugin_page]
    
    
    def create_page(self,page_id):
        if page_id == "insight_view":
            return self.create_insight_view()
        
        
    def create_insight_view(self) -> InsightView:
        
        
        