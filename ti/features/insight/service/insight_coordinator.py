from typing import List, Dict, Any
from ti.core.eventBus import EventBus
from ti.services.dataService import DataService
from ti.services.function_service import FunctionService
from ti.features.insight.service.formatter import InsightFormatService
from ti.features.insight.service.insight_interfaces import (
    IInsightServiceFactory, IInsightRecipeService, 
    IInsightCardGenerator, IInsightCardRenderer
)
from ti.features.insight.model.insight_event import (
    InsightCardGenerationStarted, RecipeLoaded, CardGenerated, 
    AllCardsGenerated, CardRendered, InsightGenerationCompleted
)
from ti.services.loggerService import LoggerService


class InsightCoordinator:
    """
    洞察卡片生成流程协调器 - 重构后版本
    采用事件驱动架构，依赖接口而不是具体实现
    """
    
    def __init__(
        self,
        bus: EventBus,
        data_service: DataService,
        function_service: FunctionService,
        format_service: InsightFormatService,
        service_factory: IInsightServiceFactory = None
    ):
        self.bus = bus
        self.data_service = data_service
        self.function_service = function_service
        self.format_service = format_service
        
        # 使用提供的工厂或创建默认工厂
        if service_factory is None:
            from ti.features.insight.service.insight_service_factory import InsightServiceFactory
            self.service_factory = InsightServiceFactory(
                data_service, function_service, format_service, bus
            )
        else:
            self.service_factory = service_factory
        
        # 创建logger
        self.logger = LoggerService("./ti/features/insight", "insight_coordinator")
        
        # 服务实例（通过接口引用）
        self.recipe_service: IInsightRecipeService = None
        self.card_generator: IInsightCardGenerator = None
        self.card_renderer: IInsightCardRenderer = None
        
        # 状态
        self.is_generating = False
        self.generated_cards = []
        
        # 订阅事件
        self._subscribe_events()
        
        self.logger.log("初始化", "InsightCoordinator初始化完成（接口依赖版本）")
    
    def _subscribe_events(self):
        """订阅相关事件"""
        # 这里可以订阅其他插件或组件发布的事件
        # 例如：当数据更新时触发卡片重新生成
        pass
    
    def start_yesterday_report_generation(self, view_component) -> List:
        """
        开始生成昨日报告卡片
        
        Args:
            view_component: 用于渲染卡片的视图组件
            
        Returns:
            List: 生成的卡片列表
        """
        if self.is_generating:
            self.logger.log("警告", "卡片生成正在进行中，忽略重复请求")
            return []
        
        self.is_generating = True
        self.generated_cards = []
        
        # 发布开始事件
        self.bus.publish(InsightCardGenerationStarted(report_type="yesterday"))
        
        try:
            # 1. 加载配方
            recipes = self._load_recipes()
            
            # 2. 初始化服务
            self._initialize_services(recipes)
            
            # 3. 生成卡片
            cards = self._generate_cards()
            
            # 4. 渲染卡片到界面
            rendered_cards = self._render_cards(cards, view_component)
            
            # 5. 发布完成事件
            self.bus.publish(InsightGenerationCompleted(success=True))
            
            self.logger.log("完成", f"成功生成并渲染 {len(rendered_cards)} 张卡片")
            return rendered_cards
            
        except Exception as e:
            self.logger.log("错误", f"卡片生成失败: {str(e)}")
            self.bus.publish(InsightGenerationCompleted(success=False, error_message=str(e)))
            return []
        finally:
            self.is_generating = False
    
    def _load_recipes(self) -> Dict[str, Any]:
        """加载洞察卡片配方"""
        self.logger.log("配方加载", "开始加载洞察卡片配方")
        
        # 使用配方服务（通过接口）
        self.recipe_service = self.service_factory.create_recipe_service()
        recipes = self.recipe_service.load_recipes()
        
        # 发布配方加载完成事件
        fixed_count = len(recipes.get("fixed_recipes", []))
        conditional_count = len(recipes.get("conditional_recipes", []))
        
        self.bus.publish(RecipeLoaded(
            fixed_recipes_count=fixed_count,
            conditional_recipes_count=conditional_count
        ))
        
        self.logger.log("配方加载", f"加载了 {conditional_count} 个条件配方和 {fixed_count} 个固定配方")
        
        return recipes
    
    def _initialize_services(self, recipes: Dict[str, Any]):
        """初始化洞察相关服务"""
        self.logger.log("服务初始化", "开始初始化洞察服务")
        
        # 使用服务工厂创建卡片生成器和渲染器
        self.card_generator = self.service_factory.create_card_generator()
        self.card_renderer = self.service_factory.create_card_renderer()
        
        self.logger.log("服务初始化", "洞察服务初始化完成")
    
    def _generate_cards(self) -> List:
        """生成洞察卡片"""
        self.logger.log("卡片生成", "开始生成洞察卡片")
        
        # 使用卡片生成器（通过接口）
        cards = self.card_generator.generate_cards()
        
        # 发布卡片生成事件
        for card in cards:
            if hasattr(card, 'id'):
                card_id = card.id
            else:
                card_id = str(id(card))
            
            self.bus.publish(CardGenerated(
                card_id=card_id,
                card_type=getattr(card, 'card_type', 'unknown'),
                card_data=card.to_dict() if hasattr(card, 'to_dict') else card
            ))
        
        # 发布所有卡片生成完成事件
        self.bus.publish(AllCardsGenerated(
            total_cards=len(cards),
            fixed_cards=len([c for c in cards if getattr(c, 'card_type', '') == 'fixed']),
            conditional_cards=len([c for c in cards if getattr(c, 'card_type', '') == 'conditional']),
            stored_cards=len([c for c in cards if getattr(c, 'card_type', '') == 'stored'])
        ))
        
        self.logger.log("卡片生成", f"成功生成 {len(cards)} 张卡片")
        return cards
    
    def _render_cards(self, cards: List, view_component) -> List:
        """渲染卡片到界面"""
        self.logger.log("卡片渲染", "开始渲染卡片到界面")
        
        # 使用卡片渲染器（通过接口）
        rendered_cards = self.card_renderer.render_cards(cards, view_component)
        
        # 发布卡片渲染事件
        for idx, card in enumerate(rendered_cards):
            card_id = getattr(cards[idx], 'id', str(idx)) if idx < len(cards) else str(idx)
            self.bus.publish(CardRendered(
                card_id=card_id,
                ui_component=card
            ))
        
        self.logger.log("卡片渲染", f"成功渲染 {len(rendered_cards)} 张卡片到界面")
        return rendered_cards
    
    def shutdown(self):
        """关闭协调器"""
        self.logger.log("关闭", "InsightCoordinator正在关闭")
        # 清理资源
        self.cache_service = None
        self.insight_engine = None
        self.insight_manager = None
        self.report_generation_service = None
        self.ui_card_factory = None