import uuid
from ti.services.sessionCache import SessionCache
from ti.features.insight.model.insight_card_generation_models import AnalyzerConfig
from ti.features.insight.model.insight_card_model import InsightCardModel


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
    
    def create_report(self,cache:SessionCache) -> dict[InsightCardModel]:
        """_summary_
        这个函数用来生成卡片报告
        Returns:
            dict: 处理好的卡片信息
        """
        # 创建固定卡片信息
        cardData: dict[InsightCardModel] = {}
        for card in self.recipe:
            config = card["analyzer_config"]
            analyzer = card["analyzer"]
            presenter = card["presenter"]
            card_id = card["id"]
            duration = card["duration"]
            
            card_result = analyzer(self.data,config)
            present_card = presenter(card_result)
            
            # 创建InsightCardModel对象
            fixed_card = InsightCardModel(
                sementic_text=present_card.sementic_key,
                judgements_texts=present_card.judgement_key,
                title_text=present_card.card_type,
                color="#3498DB",  # 默认颜色
                icon_path="",  # 默认图标路径
                icon_color="#3498DB",  # 默认图标颜色
                card_type_id=card_id,
                card_uuid=present_card.id,
                duration=duration,
                data_uuids= uuid.uuid4(),
                detector_recipe_id = analyzer,
                cache=present_card.data
            )

            cardData[fixed_card.card_uuid] = fixed_card
        
        return cardData