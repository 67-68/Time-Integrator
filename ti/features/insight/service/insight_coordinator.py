from typing import List, Dict, Any, Optional
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
from ti.features.insight.model.insight_narrative_model import InsightNarrativeModel
from ti.features.insight.model.insight_card_model import InsightCardModel
from ti.model.yaml_repository import YamlRepository
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
        
        # 创建YamlRepository用于narrative数据
        self.narrative_repository = YamlRepository[
            InsightNarrativeModel
        ](
            db_path="ti/features/insight/model/data/insight_narratives.yaml",
            model_class=InsightNarrativeModel,
            identifier_field="narrative_id"
        )
        
        # 创建YamlRepository用于insight卡片数据
        self.card_repository = YamlRepository[
            InsightCardModel
        ](
            db_path="ti/features/insight/model/data/insight_cards.yaml",
            model_class=InsightCardModel,
            identifier_field="card_uuid"
        )
        
        # 服务实例（通过接口引用）
        self.recipe_service: IInsightRecipeService = None
        self.card_generator: IInsightCardGenerator = None
        self.card_renderer: IInsightCardRenderer = None
        
        # 状态
        self.is_generating = False
        self.generated_cards = []
        
        # 订阅事件
        self._subscribe_events()
    
    def _subscribe_events(self):
        """订阅相关事件"""
        # 这里可以订阅其他插件或组件发布的事件
        # 例如：当数据更新时触发卡片重新生成
        pass
    
    def get_universal_narrative(self, key: str) -> List[str]:
        """获取通用叙事文本"""
        narrative = self.narrative_repository.get_by_id(f"universal_{key}")
        return narrative.text if narrative else []
    
    def get_specific_narrative(self, action_type: str, narrative_key: str) -> Optional[Dict[str, Any]]:
        """获取特定行动类型的叙事文本"""
        narrative_id = f"specific_{action_type}_{narrative_key}"
        narrative = self.narrative_repository.get_by_id(narrative_id)
        
        if narrative:
            # 返回与InsightNarrator兼容的格式
            return {"text": narrative.text}
        return None
    
    def get_presentation(self, action_type: str, presentation_type: str) -> Dict[str, Any]:
        """获取展示文本"""
        narrative_id = f"presentation_{action_type}_{presentation_type}"
        narrative = self.narrative_repository.get_by_id(narrative_id)
        
        if narrative:
            return {"text": narrative.text}
        return {}
    
    def start_yesterday_report_generation(self, view_component) -> List:
        """
        开始生成昨日报告卡片
        
        Args:
            view_component: 用于渲染卡片的视图组件
            
        Returns:
            List: 生成的卡片列表
        """
        if self.is_generating:
            return []
        
        self.is_generating = True
        self.generated_cards = []
        
        # 发布开始事件
        self.bus.publish_event(InsightCardGenerationStarted,InsightCardGenerationStarted(report_type="yesterday"))
        
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
            self.bus.publish_event(InsightGenerationCompleted,InsightGenerationCompleted(success=True))
            
            return rendered_cards
            
        except Exception as e:
            self.bus.publish_event(InsightGenerationCompleted,InsightGenerationCompleted(success=False, error_message=str(e)))
            print(e)
            return {}
        finally:
            self.is_generating = False
    
    def _load_recipes(self) -> Dict[str, Any]:
        """加载洞察卡片配方"""
        
        # 使用配方服务（通过接口）
        self.recipe_service = self.service_factory.create_recipe_service()
        recipes = self.recipe_service.load_recipes()
        
        # 发布配方加载完成事件
        fixed_count = len(recipes.get("fixed_recipes", []))
        conditional_count = len(recipes.get("conditional_recipes", []))
        
        self.bus.publish_event(RecipeLoaded,RecipeLoaded(
            fixed_recipes_count=fixed_count,
            conditional_recipes_count=conditional_count
        ))
        
        self.logger.log("配方加载", f"加载了 {conditional_count} 个条件配方和 {fixed_count} 个固定配方")
        
        return recipes
    
    def _initialize_services(self, recipes: Dict[str, Any]):
        """初始化洞察相关服务"""
        
        # 使用服务工厂创建卡片生成器和渲染器
        self.card_generator = self.service_factory.create_card_generator()
        self.card_renderer = self.service_factory.create_card_renderer()
    
    def _generate_cards(self) -> List:
        """生成洞察卡片"""
        
        # 使用卡片生成器（通过接口）
        cards = self.card_generator.generate_cards()
        
        # 发布卡片生成事件
        for card in cards:
            if hasattr(card, 'id'):
                card_id = card.id
            else:
                card_id = str(id(card))
            
            self.bus.publish_event(CardGenerated,CardGenerated(
                card_id=card_id,
                card_type=getattr(card, 'card_type', 'unknown'),
                card_data=card.to_dict() if hasattr(card, 'to_dict') else card
            ))
        
        # 发布所有卡片生成完成事件
        self.bus.publish_event(AllCardsGenerated,AllCardsGenerated(
            total_cards=len(cards),
            fixed_cards=len([c for c in cards if getattr(c, 'card_type', '') == 'fixed']),
            conditional_cards=len([c for c in cards if getattr(c, 'card_type', '') == 'conditional']),
            stored_cards=len([c for c in cards if getattr(c, 'card_type', '') == 'stored'])
        ))
        
        return cards
    
    def _render_cards(self, cards: dict,view_component) -> List:
        """渲染卡片到界面"""
        # 发布卡片渲染事件
        rendered_cards = self.card_renderer.render_cards(cards, view_component)
        for uuid, card in rendered_cards.items():
            self.bus.publish_event(CardRendered,CardRendered(
                card_id=card.card_id,
                card_uuid = uuid,
                ui_component=card
            ))
        
        return cards
    
    def shutdown(self):
        """关闭协调器"""
        # 清理资源
        self.cache_service = None
        self.insight_engine = None
        self.insight_manager = None
        self.report_generation_service = None
        self.ui_card_factory = None