from typing import List
from ti.features.insight.model.insight_card_generation_models import FixedCardResult, PresentedCardData
from ti.model.themes import CARD_INFO
from ti.features.insight.model.insight_card_model import InsightCardModel
from ti.features.insight.model.insight_card_repository import InsightCardRepository
from ti.services.sessionCache import SessionCache


class ReportGenerationService:
    """
    报告生成服务，负责生成昨日报告卡片
    """
    
    def __init__(
        self,
        conditional_report_generator,
        fixed_report_generator,
        cache: SessionCache
    ):
        """
        初始化报告生成服务
        
        Args:
            conditional_report_generator: 条件报告生成器
            fixed_report_generator: 固定报告生成器
            cache: 会话缓存
        """
        self.conditional_report_generator = conditional_report_generator
        self.fixed_report_generator = fixed_report_generator
        self.cache = cache
        self.card_repository = InsightCardRepository()
        
        # 持有卡片状态
        self.cards: List[PresentedCardData] = []
    
    def create_yesterday_report(self) -> List:
        """
        创建昨日报告
        
        Returns:
            list: 生成的卡片列表
        """
        # 获取固定卡片
        fixed_cards = self.fixed_report_generator.create_report(self.cache)
        
        # 创建条件卡片
        cond_cards = self.conditional_report_generator.create_report()
        
        # 加载存储的卡片
        stored_cards = self._load_stored_cards()
        
        # 卡片汇总（新生成的卡片 + 存储的卡片）
        self.cards = cond_cards + fixed_cards + stored_cards
        
        print(f"生成报告: {len(cond_cards)} 条件卡片, {len(fixed_cards)} 固定卡片, {len(stored_cards)} 存储卡片")
        
        return self.cards
    
    def get_cards(self) -> List[PresentedCardData]:
        """
        获取生成的卡片
        
        Returns:
            List[PresentedCardData]: 卡片列表
        """
        return self.cards
    
    def _load_stored_cards(self) -> List[PresentedCardData]:
        """
        加载存储的卡片并转换为PresentedCardData格式
        
        Returns:
            List[PresentedCardData]: 转换后的卡片列表
        """
        stored_cards = []
        
        # 获取所有存储的卡片
        all_stored_cards = self.card_repository.get_all()
        
        for card_uuid, insight_card in all_stored_cards.items():
            # 将InsightCardModel转换为PresentedCardData格式
            presented_card = PresentedCardData(
                card_type=CARD_INFO,
                judgement_key=[],  # 存储的卡片可能没有judgement_key
                sementic_key=insight_card.card_type_id,
                data={
                    "title": insight_card.title_text,
                    "sementic_text": insight_card.sementic_text,
                    "judgements_texts": insight_card.judgements_texts,
                    "color": insight_card.color,
                    "icon_path": insight_card.icon_path,
                    "icon_color": insight_card.icon_color
                },
                weight=1.0,  # 默认权重
                id=insight_card.card_uuid
            )
            stored_cards.append(presented_card)
        
        return stored_cards