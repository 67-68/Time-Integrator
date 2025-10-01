import uuid
from typing import Dict, Any
from ti.features.insight.view.insight_card import InsightCard
from ti.features.insight.presenter.insight_card_presenter import InsightPresenter
from ti.core.eventBus import EventBus
from ti.features.insight.service.formatter import InsightFormatService


class InsightCardFactory:
    """
    UI卡片工厂服务，负责数据翻译和UI卡片创建
    """
    
    def __init__(
        self,
        format_service: InsightFormatService,
        event_bus: EventBus
    ):
        """
        初始化UI卡片工厂
        
        Args:
            format_service: 格式化服务
            event_bus: 事件总线
        """
        self.format = format_service
        self.bus = event_bus
    
    def create_ui_card(self, card_data, parent_view) -> Dict[str, Any]:
        """
        创建UI卡片
        
        Args:
            card_data: 卡片数据（可以是dataclass或字典）
            parent_view: 父视图
            
        Returns:
            Dict: 包含卡片和presenter的字典
        """
        # 格式化数据
        formatted_data = self.format.format_card(card_data)
        
        # 创建UI卡片
        card = self._create_card_ui(formatted_data, parent_view)
        
        # 发布卡片创建事件
        self._publish_card_event(card, card_data)
        
        # 设置卡片presenter
        card_presenter = self._setup_card_presenter(card)
        
        return {
            "card": card,
            "presenter": card_presenter,
            "card_data": card_data
        }
    
    def _create_card_ui(self, formatted_data, parent_view):
        """创建UI卡片实例"""
        return InsightCard(formatted_data, parent=parent_view)
    
    def _publish_card_event(self, card, original_card_data):
        """发布卡片创建事件"""
        self.bus.publish("insight_card_ui_created", (card, original_card_data))
    
    def _setup_card_presenter(self, card):
        """设置卡片presenter"""
        # 创建卡片presenter
        return InsightPresenter(card)