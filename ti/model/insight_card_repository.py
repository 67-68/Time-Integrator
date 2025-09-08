from datetime import datetime
from ti.core.Interfaces.json_repository_interface import JsonRepositoryInterface
from ti.services.dataAccess.dataAccess import getData, saveData
from ti.model.insight_card_model import InsightCardModel


class InsightCardRepository(JsonRepositoryInterface):
    def __init__(self):
        """
        存储已生成的insight卡片
        管理洞察卡片的历史记录
        """
        self.cards = {}
        self.cards = self.load()
        super().__init__()

    @property
    def filePath(self):
        return "model/data/insight_cards.json"
    
    def save(self, data: dict[str, InsightCardModel] = None):
        """
        一次性保存所有卡片数据
        """
        if data is not None:
            self.cards = data
        
        raw_data = {
            card_uuid: {
                "sementic_text": card.sementic_text,
                "judgements_texts": card.judgements_texts,
                "title_text": card.title_text,
                "color": card.color,
                "icon_path": card.icon_path,
                "icon_color": card.icon_color,
                "card_type_id": card.card_type_id,
                "card_uuid": card.card_uuid
            }
            for card_uuid, card in self.cards.items()
        }
        
        saveData(raw_data, self.filePath)
        print(f"保存了洞察卡片数据，共 {len(raw_data)} 张卡片")
    
    def load(self) -> dict[str, InsightCardModel]:
        """
        从文件加载所有卡片数据
        """
        try:
            raw_data = getData(self.filePath)
            for card_uuid, card_dict in raw_data.items():
                if card_dict:
                    self.cards[card_uuid] = InsightCardModel(
                        sementic_text=card_dict.get("sementic_text", ""),
                        judgements_texts=card_dict.get("judgements_texts", []),
                        title_text=card_dict.get("title_text", ""),
                        color=card_dict.get("color", "#3498DB"),
                        icon_path=card_dict.get("icon_path", ""),
                        icon_color=card_dict.get("icon_color", "#3498DB"),
                        card_type_id=card_dict.get("card_type_id", ""),
                        card_uuid=card_dict.get("card_uuid", "")
                    )
        except Exception as ex:
            print(f"加载洞察卡片失败: {ex}")
            self.cards = {}
        
        return self.cards
    
    def add_card(self, card: InsightCardModel):
        """
        添加新的卡片记录
        自动保存
        """
        self.cards[card.card_uuid] = card
        print(f"添加洞察卡片: {card.card_uuid}")
        self.save()
        
    def get_by_id(self, card_uuid: str) -> InsightCardModel | None:
        """
        通过卡片UUID获取记录
        """
        import copy
        card = self.cards.get(card_uuid)
        return copy.deepcopy(card) if card else None

    def get_all(self) -> dict[str, InsightCardModel]:
        """
        获取所有卡片记录
        """
        import copy
        return copy.deepcopy(self.cards)
        
    def delete(self, card_uuid: str):
        """
        删除指定的卡片记录
        """
        if card_uuid in self.cards:
            del self.cards[card_uuid]
            self.save()
            print(f"删除洞察卡片: {card_uuid}")
        else:
            print(f"未找到卡片记录: {card_uuid}")
    
    def get_by_card_type(self, card_type_id: str) -> list[InsightCardModel]:
        """
        按卡片类型ID获取卡片记录
        """
        return [
            card for card in self.cards.values() 
            if card.card_type_id == card_type_id
        ]
    
    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> list[InsightCardModel]:
        """
        按日期范围获取卡片记录
        注意：InsightCardModel当前没有日期字段，此方法为预留接口
        """
        # 如果未来InsightCardModel添加了日期字段，可以在此实现日期过滤
        return list(self.cards.values())