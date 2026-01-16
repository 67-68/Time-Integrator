from ti.core.eventBus import EventBus
from ti.model.yaml_repository import YamlRepository
from ti.features.insight.model.insight_event import SaveInsightCard
from ti.features.insight.model.insight_card_model import InsightCardModel
from ti.features.insight.service.uiCardFactory import InsightCardFactory
from ti.features.insight.view.insight_view import InsightView
from ti.services.loggerService import LoggerService


class InsightPresenter():
    """
    简化版InsightPresenter - 重构后版本
    主要职责：处理卡片保存事件和UI卡片管理
    卡片生成逻辑已迁移到InsightCoordinator
    """
    
    def __init__(
        self,
        bus: EventBus,
        view: InsightView,
        ui_card_factory: InsightCardFactory
    ):
        self.bus = bus
        self.view = view
        self.ui_card_factory = ui_card_factory
        
        # 创建YamlRepository用于insight卡片数据
        self.card_repository = YamlRepository[
            InsightCardModel
        ](
            db_path="ti/features/insight/model/data/insight_cards.yaml",
            model_class=InsightCardModel,
            identifier_field="card_uuid"
        )
        
        # 创建logger
        self.logger = LoggerService("./ti/features/insight", "card_presenter")
        
        # 订阅保存卡片事件
        self.bus.subscribe_event(SaveInsightCard, self._on_save_insight_card)
        
        # 当前显示的卡片
        self.current_cards = {}
        
        self.logger.log("初始化", "简化版卡片Presenter初始化完成")
    
    def render_cards(self, cards_data) -> dict:
        """
        渲染卡片到界面
        
        Args:
            cards_data: 卡片数据列表
            
        Returns:
            dict: 渲染后的卡片字典
        """
        self.logger.log("卡片渲染", "开始渲染卡片到界面")
        
        rendered_cards = {}
        
        for idx, card_data in enumerate(cards_data):
            # 使用UI工厂创建卡片
            ui_result = self.ui_card_factory.create_ui_card(
                card_data, self.view
            )
            
            rendered_cards[idx] = ui_result["card"]
            
            # 保存引用，防止被垃圾回收
            self.view.add_card(ui_result["card"])
        
        self.current_cards = rendered_cards
        self.logger.log("卡片渲染", f"成功渲染 {len(rendered_cards)} 张卡片到界面")
        return rendered_cards
    
    def save_cards(self, cards):
        """保存卡片到仓库"""
        if not cards:
            self.logger.log("卡片保存", "没有卡片需要保存")
            return
        
        try:
            # 使用YamlRepository保存每张卡片
            for card in cards:
                if hasattr(card, 'card_uuid'):
                    self.card_repository.save(card)
            
            self.logger.log("卡片保存", f"成功保存 {len(cards)} 张卡片")
            
        except Exception as e:
            self.logger.log("卡片保存错误", f"保存卡片时发生错误: {str(e)}")
    
    def _on_save_insight_card(self, event: SaveInsightCard):
        """
        处理保存洞察卡片事件
        
        Args:
            event: SaveInsightCard事件，包含card_uuid
        """
        self.logger.log("事件处理", f"接收到保存卡片事件: {event.event_id}")
        
        if isinstance(event, SaveInsightCard):
            card_uuid = event.card_uuid
            
            # 这里可以扩展为从当前活跃卡片中查找并保存特定卡片
            # 目前简化处理，保存所有当前卡片
            if self.current_cards:
                self.save_cards(list(self.current_cards.values()))
                self.logger.log("事件保存", f"保存了 {len(self.current_cards)} 张卡片")
            else:
                self.logger.log("事件保存", "没有活跃卡片需要保存")