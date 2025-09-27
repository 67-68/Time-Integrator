import uuid
from typing import Dict, Any
from ti.features.insight.model.insight_card_generation_models import FixedCardResult, PresentedCardData
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
    
    def create_ui_card(self, card_data, parent_view, cache) -> Dict[str, Any]:
        """
        创建UI卡片
        
        Args:
            card_data: 卡片数据（可以是dataclass或字典）
            parent_view: 父视图
            cache: 会话缓存
            
        Returns:
            Dict: 包含卡片和presenter的字典
        """
        # 适配卡片数据
        card_dict, card_data_for_presenter = self._adapt_card_data(card_data)
        
        # 格式化数据
        formatted_data = self.format.format_card(card_dict)
        
        # 创建UI卡片
        card = self._create_card_ui(formatted_data, parent_view)
        
        # 发布卡片创建事件
        self._publish_card_event(card, cache, card_data)
        
        # 设置卡片presenter
        card_presenter = self._setup_card_presenter(card, card_data_for_presenter)
        
        return {
            "card": card,
            "presenter": card_presenter,
            "card_data": card_data_for_presenter
        }
    
    def _adapt_card_data(self, card_data):
        """适配不同类型的卡片数据"""
        if isinstance(card_data, (PresentedCardData, FixedCardResult)):
            # 如果是dataclass对象，转换为字典
            card_dict = self._convert_dataclass_to_dict(card_data)
            
            # 对于FixedCardResult，添加额外的字段
            if isinstance(card_data, FixedCardResult):
                card_dict["duration"] = card_data.duration
                card_dict["card_type_id"] = card_data.card_type_id
            
            return card_dict, card_dict
        else:
            # 如果是字典，直接使用
            return card_data, card_data
    
    def _create_card_ui(self, formatted_data, parent_view):
        """创建UI卡片实例"""
        return InsightCard(formatted_data, parent=parent_view)
    
    def _publish_card_event(self, card, cache, original_card_data):
        """发布卡片创建事件"""
        self.bus.publish("insight_card_ui_created", (card, cache, original_card_data))
    
    def _setup_card_presenter(self, card, card_data_for_presenter):
        """设置卡片presenter"""
        # 设置卡片元数据
        card_data_for_presenter["card_type_id"] = card_data_for_presenter["sementic_key"]
        card_data_for_presenter["card_uuid"] = str(uuid.uuid4())
        
        # 创建卡片presenter
        return InsightPresenter(card)
    
    def _convert_dataclass_to_dict(self, card_data) -> Dict[str, Any]:
        """
        将dataclass对象转换为字典
        
        Args:
            card_data: dataclass对象
            
        Returns:
            Dict: 转换后的字典
        """
        return {
            "card_type": card_data.card_type,
            "judgement_key": card_data.judgement_key,
            "sementic_key": card_data.sementic_key,
            "data": card_data.data,
            "weight": card_data.weight,
            "id": card_data.id
        }