from PyQt6.QtCore import QObject
from typing import Optional

from ti.features.insight.model.insight_card_model import InsightCardModel
from ti.features.insight.view.insight_card import InsightCard


class InsightCardPresenter(QObject):
    def __init__(
        self,
        card_ui: InsightCard,
        card_data: InsightCardModel, # 创建insight card所用的Model presentation
        parent = None
    ):
        """_summary_
        卡片逻辑类，负责管理卡片的UI
        Args:
            parent (_type_, optional): _description_. Defaults to None.
        """
        super().__init__(parent)
        self.ui = card_ui
        
        self.card_data = card_data
        self.insight_card_model: Optional[InsightCardModel] = None
        
        # 拆包数据并创建数据模型
        self.insight_card_model = card_data
            
    def get_card_data(self):
        return self.card_data
    
    def get_insight_card_model(self) -> Optional[InsightCardModel]:
        """
        获取创建的InsightCardModel实例
        """
        return self.insight_card_model