from ti.core.Interfaces.extension_Interface import ExtensionInterface
from ti.model.plugin.function_contributions import FunctionContribution
from ti.model.plugin.function_provider_interface import IFunctionExtension
from ti.model.plugin.page_extension_interface import IPageExtension
from ti.features.insight.view.insight_view import InsightView
from ti.model.core_pages import CoreView
from ti.model.plugin.page_contributions import PageContribution
from ti.services.dataService import DataService
from ti.features.insight.service.formatter import InsightFormatService
from ti.services.symbol_service import SymbolService
from ti.services.loggerService import LoggerService
from ti.services.function_service import FunctionService
from ti.features.insight.service.insight_coordinator import InsightCoordinator


class InsightPlugin(
    IPageExtension,
    IFunctionExtension,
):
    def __init__(
        self,
        symbol_service: SymbolService,
        data_service: DataService,
        function_service: FunctionService,
        format: InsightFormatService
    ):
        super().__init__()
        self.symbol = symbol_service
        self.data_service = data_service
        self.function_service = function_service
        self.format = format
        
        # 创建logger
        self.logger = LoggerService("./ti/features/insight", "insight")
        self.logger.log("初始化", "InsightPlugin初始化完成")
        
        # InsightCoordinator将在initialize时创建
        self.coordinator = None
    
    def initialize(self, eventBus):
        self.bus = eventBus
        
        # 创建InsightCoordinator
        self.coordinator = InsightCoordinator(
            bus=self.bus,
            data_service=self.data_service,
            function_service=self.function_service,
            format_service=self.format
        )
        
        self.bus.publish("PagePluginRegistered", self.page_contributions)
    
        
    def shutdown(self):
        if self.coordinator:
            self.coordinator.shutdown()
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
        """
        创建洞察视图 - 重构后版本
        使用InsightCoordinator进行事件驱动的卡片生成
        """
        self.logger.log("创建视图", "开始创建洞察视图（重构后）")
        
        # 创建视图组件
        self.view = InsightView()
        
        # 使用Coordinator进行卡片生成
        if self.coordinator:
            cards = self.coordinator.start_yesterday_report_generation(self.view)
            self.logger.log("卡片生成", f"Coordinator成功生成 {len(cards)} 张卡片")
        else:
            self.logger.log("错误", "Coordinator未初始化，无法生成卡片")
            cards = []
        
        return self.view
    
    @property
    def function_contributions(self):
        return [
            FunctionContribution(
                self.get_insight_cache,
                "get_insight_cache"
            )
        ]
        
    def get_insight_cache(self):
        """获取洞察缓存 - 现在通过服务工厂创建"""
        # 由于现在使用接口依赖，缓存服务由具体实现管理
        # 如果需要获取缓存，可以通过工厂创建新的缓存服务实例
        from ti.features.insight.service.insightCacheService import InsightCacheService
        return InsightCacheService()