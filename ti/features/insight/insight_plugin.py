from ti.core.Interfaces.extension_Interface import ExtensionInterface
from ti.model.plugin.function_contributions import FunctionContribution
from ti.model.plugin.function_provider_interface import IFunctionExtension
from ti.model.plugin.page_extension_interface import IPageExtension
from ti.features.insight.presenter.cardPresenter import InsightPresenter
from ti.features.insight.view.insight_view import InsightView
from ti.model.core_pages import CoreView
from ti.model.plugin.page_contributions import PageContribution
from ti.services.dataService import DataService
from ti.features.insight.service.insightCacheService import InsightCacheService
from ti.features.insight.service.insightManager import InsightManager
from ti.features.insight.service.insightEngine import InsightEngine
from ti.features.insight.service.formatter import InsightFormatService
from ti.services.serviceContainer import ServiceContainer
from ti.services.symbol_service import SymbolService
from ti.services.loggerService import LoggerService
from ti.services.function_service import FunctionService


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
    
    def initialize(self, eventBus):
        self.bus = eventBus
        self.bus.publish("PagePluginRegistered", self.page_contributions)
        self.logger.log("事件总线", "事件总线初始化完成并发布页面插件注册事件")
    
        
    def shutdown(self):
        self.logger.log("关闭", "InsightPlugin正在关闭")
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
        self.logger.log("创建视图", "开始创建洞察视图")
        self.view = InsightView()
        
        # 通过function service获取detector factory
        try:
            get_detector_factory_func = self.function_service.get_function("get_detector_factory")
            detector_factory = get_detector_factory_func()
            self.logger.log("获取工厂", "成功从function service获取detector factory")
        except Exception as e:
            self.logger.log("错误", f"获取detector factory失败: {e}")
            raise
        
        # 创建缓存服务
        self.cache = InsightCacheService()
        
        # 创建引擎和管理器
        self.engine = InsightEngine(self.cache, detector_factory)
        self.manager = InsightManager(self.cache)
        
        # 创建配方仓库
        from ti.model.yaml_repository import YamlRepository
        from ti.features.insight.model.insight_card_recipe_models import FixedRecipe, ConditionalRecipe
        
        # 使用YamlRepository加载配方数据
        recipe_repo = YamlRepository(
            "ti/features/insight/model/data/insight_card_recipes.yaml", 
            dict,  # 使用dict作为模型类，因为我们手动处理结构
            identifier_field="insight_card_recipes"
        )
        
        # 获取配方数据
        recipes_data = recipe_repo.get_by_id("insight_card_recipes")
        if recipes_data and "insight_card_recipes" in recipes_data:
            recipes_container = recipes_data["insight_card_recipes"]
            
            # 解析固定配方
            fixed_recipe = []
            if "fixed_recipes" in recipes_container:
                for recipe_data in recipes_container["fixed_recipes"]:
                    fixed_recipe.append(FixedRecipe(**recipe_data))
            
            # 解析条件配方
            cond_recipe = []
            if "conditional_recipes" in recipes_container:
                for recipe_data in recipes_container["conditional_recipes"]:
                    cond_recipe.append(ConditionalRecipe(**recipe_data))
        else:
            cond_recipe = []
            fixed_recipe = []
        
        self.logger.log("配方加载", f"加载了 {len(cond_recipe)} 个条件配方和 {len(fixed_recipe)} 个固定配方")
        
        # 创建报告生成器
        from ti.features.insight.presenter.conditional_cardPresenter import Conditional_ReportGenerator
        from ti.features.insight.presenter.fixed_cardPresenter import Fixed_ReportGenerator
        from ti.services.sessionCache import SessionCache
        from ti.features.insight.service.reportGenerationService import ReportGenerationService
        
        session_cache = SessionCache()
        yesterday_data = self.data_service.get_yesterday_AU()
        
        conditional_report_generator = Conditional_ReportGenerator(
            yesterday_data,
            cond_recipe,
            self.engine,
            self.manager,
            session_cache
        )
        
        fixed_report_generator = Fixed_ReportGenerator(
            yesterday_data,
            fixed_recipe
        )
        
        # 创建报告生成服务
        report_generation_service = ReportGenerationService(
            conditional_report_generator,
            fixed_report_generator,
            session_cache
        )
        
        # 创建UI卡片工厂
        from ti.features.insight.service.uiCardFactory import InsightCardFactory
        ui_card_factory = InsightCardFactory(self.format, self.bus)
        
        # 创建卡片仓库
        from ti.features.insight.model.insight_card_repository import InsightCardRepository
        card_repository = InsightCardRepository()
        
        # 创建卡片presenter
        self.presenter = InsightPresenter(
            self.data_service,
            self.bus,
            self.view,
            self.format,
            report_generation_service,
            ui_card_factory,
            card_repository
        )
        
        # 生成并显示卡片
        cards = self.presenter.create_yesterday_report()
        if cards: 
            self.logger.log("卡片生成", f"成功生成 {len(cards)} 张卡片")
        else:
            self.logger.log("卡片生成", "没有卡片被生成")
        
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
        return self.cache