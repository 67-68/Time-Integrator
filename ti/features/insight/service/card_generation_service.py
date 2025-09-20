from ti.features.insight.presenter.insight_card_presenter import InsightPresenter
from ti.features.insight.view.insight_card import InsightCard


class InsightCardGeneration:
    def __init__(self):
        """
        这个类全权管理卡片创建
        它负责创建卡片并最终返回UI卡片
        """
        
        
    def create_today_cards(self) -> list[InsightPresenter]:
        