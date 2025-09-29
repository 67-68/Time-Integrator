from typing import List, Any
from ti.features.insight.service.insight_interfaces import IInsightCardGenerator
from ti.services.loggerService import LoggerService


class InsightCardGenerator(IInsightCardGenerator):
    """洞察卡片生成器实现"""
    
    def __init__(self, report_generation_service):
        self.report_generation_service = report_generation_service
        self.logger = LoggerService("./ti/features/insight", "card_generator")
    
    def generate_cards(self) -> List[Any]:
        """生成洞察卡片"""
        self.logger.log("卡片生成", "开始生成洞察卡片")
        
        # 使用报告生成服务创建卡片
        cards = self.report_generation_service.create_yesterday_report()
        return cards