from typing import List
from ti.features.insight.presenter.conditional_cardPresenter import Conditional_ReportGenerator
from ti.features.insight.presenter.fixed_cardPresenter import Fixed_ReportGenerator
from ti.model.themes import CARD_INFO
from ti.features.insight.model.insight_card_model import InsightCardModel
from ti.model.yaml_repository import YamlRepository
from ti.services.sessionCache import SessionCache


class ReportGenerationService:
    """
    报告生成服务，负责生成昨日报告卡片
    """
    
    def __init__(
        self,
        conditional_report_generator: Conditional_ReportGenerator,
        fixed_report_generator: Fixed_ReportGenerator,
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
        self.card_repository = YamlRepository[
            InsightCardModel
        ](
            db_path="ti/features/insight/model/data/insight_cards.yaml",
            model_class=InsightCardModel,
            identifier_field="card_uuid"
        )
        
        # 持有卡片状态
        self.cards: dict[InsightCardModel] = {}
    
    def create_yesterday_report(self) -> List:
        """
        创建昨日报告
        
        Returns:
            list: 生成的卡片列表
        """
        # 获取固定卡片
        fixed_cards = self.fixed_report_generator.create_report(self.cache)
        for uuid,card in fixed_cards.items():
            self.cards[uuid] = card
        
        # 创建条件卡片
        cond_cards = self.conditional_report_generator.create_report()
        for uuid,card in cond_cards.items():
            self.cards[uuid] = card
        
        # 加载存储的卡片
        stored_cards = self._load_stored_cards()
        for uuid,card in stored_cards.items():
            self.cards[uuid] = card
        
        # 卡片汇总（新生成的卡片 + 存储的卡片）
        # 假设生成的卡片都是Dict
        
        
        print(f"生成报告: {len(cond_cards)} 条件卡片, {len(fixed_cards)} 固定卡片, {len(stored_cards)} 存储卡片")
        
        return self.cards
    
    def get_cards(self) -> List[InsightCardModel]:
        """
        获取生成的卡片
        
        Returns:
            List[PresentedCardData]: 卡片列表
        """
        return self.cards
    
    def _load_stored_cards(self) -> dict[str, InsightCardModel]:
        """
        加载存储的卡片并转换为字典格式
        
        Returns:
            dict[str, InsightCardModel]: 卡片UUID到卡片模型的映射
        """
        cards_list = self.card_repository.get_all()
        return {card.card_uuid: card for card in cards_list}
        
        