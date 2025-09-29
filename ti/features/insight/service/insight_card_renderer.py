from typing import List, Any
from ti.features.insight.service.insight_interfaces import IInsightCardRenderer
from ti.services.loggerService import LoggerService


class InsightCardRenderer(IInsightCardRenderer):
    """洞察卡片渲染器实现"""
    
    def __init__(self, ui_card_factory, cache_service):
        self.ui_card_factory = ui_card_factory
        self.cache_service = cache_service
        self.logger = LoggerService("./ti/features/insight", "card_renderer")
    
    def render_cards(self, cards_data: List[Any], view_component: Any) -> List[Any]:
        """渲染卡片到界面"""
        self.logger.log("卡片渲染", "开始渲染卡片到界面")
        
        rendered_cards = []
        
        for idx, card_data in enumerate(cards_data):
            # 使用UI工厂创建卡片
            ui_result = self.ui_card_factory.create_ui_card(
                card_data, view_component, self.cache_service
            )
            
            rendered_cards.append(ui_result["card"])
            
            # 保存引用，防止被垃圾回收
            view_component.add_card(ui_result["card"])
        
        self.logger.log("卡片渲染", f"成功渲染 {len(rendered_cards)} 张卡片到界面")
        return rendered_cards