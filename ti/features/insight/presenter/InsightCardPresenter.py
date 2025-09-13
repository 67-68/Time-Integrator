from PyQt6.QtCore import QObject
from typing import Optional

from ti.features.insight.model.insight_card_model import InsightCardModel
from ti.features.insight.view.insight_card import InsightCard


class InsightCardPresenter(QObject):
    def __init__(
        self,
        card_ui: InsightCard,
        card_data: dict, # 创建insight card所用的presentation
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
        self._unpack_card_data()
        
    def _unpack_card_data(self):
        """
        拆包传入的card_data，根据@ti/view/views/analysis/trendCard.py的结构
        创建InsightCardModel数据模型
        """
        try:
            # 从card_data中提取数据，参考trendCard.py的拆包逻辑
            presentation = self.card_data.get("presentation", {})
            text_data = self.card_data.get("text", {})
            
            # 提取语义文本
            sementic_text = text_data.get("sementic", "")
            
            # 提取判断文本列表
            judgements_texts = text_data.get("judgement", [])
            
            # 提取标题文本
            title_text = presentation.get("title", "")
            
            # 提取颜色
            color = presentation.get("color", "#3498DB")  # 默认颜色
            
            # 提取图标路径
            icon_path = presentation.get("icon", "")
            
            # 提取图标颜色
            icon_color = presentation.get("color", "#3498DB")  # 通常与主颜色相同
            
            # 提取卡片类型ID（sementic_key）
            card_type_id = self.card_data.get("sementic_key", "")
            
            # 提取卡片UUID
            card_uuid = self.card_data.get("card_uuid", "")
            
            # 创建InsightCardModel实例
            self.insight_card_model = InsightCardModel(
                sementic_text=sementic_text,
                judgements_texts=judgements_texts,
                title_text=title_text,
                color=color,
                icon_path=icon_path,
                icon_color=icon_color,
                card_type_id=card_type_id,
                card_uuid=card_uuid
            )
            
            print(f"成功创建InsightCardModel: {self.insight_card_model}")
            
        except Exception as e:
            print(f"拆包card_data失败: {e}")
            self.insight_card_model = None
    
    def get_card_data(self):
        return self.card_data
    
    def get_insight_card_model(self) -> Optional[InsightCardModel]:
        """
        获取创建的InsightCardModel实例
        """
        return self.insight_card_model