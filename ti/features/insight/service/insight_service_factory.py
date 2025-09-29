from ti.features.insight.service.insight_interfaces import IInsightServiceFactory, IInsightRecipeService, IInsightCardGenerator, IInsightCardRenderer
from ti.features.insight.service.insight_recipe_service import InsightRecipeService
from ti.features.insight.service.insight_card_generator import InsightCardGenerator
from ti.features.insight.service.insight_card_renderer import InsightCardRenderer
from ti.services.loggerService import LoggerService


class InsightServiceFactory(IInsightServiceFactory):
    """洞察服务工厂实现"""
    
    def __init__(self, data_service, function_service, format_service, bus):
        self.data_service = data_service
        self.function_service = function_service
        self.format_service = format_service
        self.bus = bus
        self.logger = LoggerService("./ti/features/insight", "service_factory")
    
    def create_recipe_service(self) -> IInsightRecipeService:
        """创建配方服务"""
        self.logger.log("服务创建", "创建配方服务")
        return InsightRecipeService()
    
    def create_card_generator(self) -> IInsightCardGenerator:
        """创建卡片生成器"""
        self.logger.log("服务创建", "创建卡片生成器")
        
        # 需要先创建必要的服务
        from ti.features.insight.service.insightCacheService import InsightCacheService
        from ti.features.insight.service.insightEngine import InsightEngine
        from ti.features.insight.service.insightManager import InsightManager
        from ti.features.insight.presenter.conditional_cardPresenter import Conditional_ReportGenerator
        from ti.features.insight.presenter.fixed_cardPresenter import Fixed_ReportGenerator
        from ti.services.sessionCache import SessionCache
        from ti.features.insight.service.card_generation import ReportGenerationService
        
        # 获取detector factory
        get_detector_factory_func = self.function_service.get_function("get_detector_factory")
        detector_factory = get_detector_factory_func()
        
        # 创建缓存服务
        cache_service = InsightCacheService()
        
        # 创建引擎和管理器
        insight_engine = InsightEngine(cache_service, detector_factory)
        insight_manager = InsightManager(cache_service)
        
        # 加载配方
        recipe_service = self.create_recipe_service()
        recipes = recipe_service.load_recipes()
        
        # 创建报告生成器
        session_cache = SessionCache()
        yesterday_data = self.data_service.get_yesterday_AU()
        
        conditional_report_generator = Conditional_ReportGenerator(
            yesterday_data,
            recipes["conditional_recipes"],
            insight_engine,
            insight_manager,
            session_cache
        )
        
        fixed_report_generator = Fixed_ReportGenerator(
            yesterday_data,
            recipes["fixed_recipes"]
        )
        
        # 创建报告生成服务
        report_generation_service = ReportGenerationService(
            conditional_report_generator,
            fixed_report_generator,
            session_cache
        )
        
        return InsightCardGenerator(report_generation_service)
    
    def create_card_renderer(self) -> IInsightCardRenderer:
        """创建卡片渲染器"""
        self.logger.log("服务创建", "创建卡片渲染器")
        
        from ti.features.insight.service.uiCardFactory import InsightCardFactory
        from ti.features.insight.service.insightCacheService import InsightCacheService
        
        # 创建UI卡片工厂
        ui_card_factory = InsightCardFactory(self.format_service, self.bus)
        
        # 创建缓存服务
        cache_service = InsightCacheService()
        
        return InsightCardRenderer(ui_card_factory, cache_service)