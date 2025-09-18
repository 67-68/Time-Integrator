from ti.core.Interfaces.extension_Interface import ExtensionInterface
from ti.core.Interfaces.page_extension_interface import IPageExtension
from ti.core.Interfaces.path_register_provider_interface import IPathRegisterProvider
from ti.features.detector.detectorFactory import DetectorFactory
from ti.features.insight.insight_path_register import InsightPathRegister
from ti.features.insight.presenter.cardPresenter import CardPresenter
from ti.features.insight.view.insight_view import InsightView
from ti.features.yaml_database.service.yaml_parser_service import YamlParser
from ti.model.core_pages import CoreView
from ti.model.page_contributions import PageContribution
from ti.services.dataAccess.dataService import DataService
from ti.services.dataAccess.insightCacheService import InsightCacheService
from ti.services.dataAccess.insightManager import InsightManager
from ti.services.engine.insightEngine import InsightEngine
from ti.services.formatter import FormatService
from ti.services.serviceContainer import ServiceContainer
from ti.services.symbol_service import SymbolService


class InsightPlugin(
    IPathRegisterProvider,
    IPageExtension
):
    def __init__(
        self,
        yaml_parser: YamlParser,
        symbol_service: SymbolService,
        data_service: DataService,
        fac: DetectorFactory,
        format: FormatService
    ):
        super().__init__()
        self.yaml = yaml_parser
        self.symbol = symbol_service
        self.data_service = data_service
        self.fac = fac
        self.format = format
    
    def initialize(self, eventBus):
        self.bus = eventBus
        self.bus.publish("PagePluginRegistered", self.page_contributions)
    
        
    def shutdown(self):
        return super().shutdown()
    
    @property
    def name(self):
        return "insight_plugin"
    
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
        self.view = InsightView()
        self.cache = InsightCacheService()
        self.engine = InsightEngine(self.cache,self.fac)
        self.manager = InsightManager(self.cache)
        self.presenter = CardPresenter(
            self.yaml,
            self.symbol,
            self.data_service,
            self.engine,
            self.manager,
            self.bus,
            self.view,
            self.format
        )
        
        # 生成并显示卡片
        self.presenter.create_yesterday_report()
        
        return self.view
    
    @staticmethod
    def register_class():
        return InsightPathRegister
        
        
        