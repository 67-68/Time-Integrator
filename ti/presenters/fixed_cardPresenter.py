from ti.services.sessionCache import SessionCache
from ti.model.insight_card_generation_models import FixedCardResult, AnalyzerConfig


class Fixed_ReportGenerator():
    """_summary_
    这个类用来承载fixed card
    """
    def __init__(
        self,
        data, #需要处理的数据
        recipe: dict #固定卡片的配方
    ):
        self.data = data
        self.recipe = recipe
    
    def create_report(self,cache:SessionCache) -> list[FixedCardResult]:
        """_summary_
        这个函数用来生成卡片报告
        Returns:
            dict: 处理好的卡片信息
        """
        # 创建固定卡片信息
        cardData: list[FixedCardResult] = []
        for card in self.recipe:
            config = card["analyzer_config"]
            analyzer = card["analyzer"]
            presenter = card["presenter"]
            card_id = card["id"]
            duration = card["duration"]
            
            card_result = analyzer(self.data,config)
            present_card = presenter(card_result)
            
            # 创建FixedCardResult对象
            fixed_card = FixedCardResult(
                card_type=present_card.card_type,
                judgement_key=present_card.judgement_key,
                sementic_key=present_card.sementic_key,
                data=present_card.data,
                weight=present_card.weight,
                id=present_card.id,
                duration=duration,
                card_type_id=card_id
            )
            
            sementic_key = present_card.sementic_key

            # 先把sementic key存进去，不存卡片id. 以后要改
            cache.store(sementic_key,fixed_card)
            
            cardData.append(fixed_card)
        
        return cardData