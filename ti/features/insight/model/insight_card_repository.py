import uuid
from datetime import datetime
from ti.core.Interfaces.view.json_repository_interface import IJsonRepository
from ti.services.dataAccess import getData, saveData
from ti.features.insight.model.insight_card_model import InsightCardModel


class InsightCardRepository(IJsonRepository):
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
        return "/Users/lennon/Projects/Time_Integrater/ti/features/insight/model/data/insight_cards.json"
    
    def save(self, data: dict[str, InsightCardModel] = None):
        """
        一次性保存所有卡片数据
        序列化
        """
        if data is not None:
            self.cards = data
        
        new_data = {}
        
        for uuid in data:
            new_data[uuid] = data[uuid].model_dump()
            
        
        saveData(new_data, self.filePath)
        print(f"保存了洞察卡片数据，共 {len(new_data)} 张卡片")
    
    def load(self) -> dict[str, InsightCardModel]:
        """
        从文件加载所有卡片数据
        反序列化
        """
        try:
            raw_data = getData(self.filePath)
            for card_uuid, card_dict in raw_data.items():
                if card_dict:
                    # 使用from_dict方法来自动处理所有字段，包括新增的元数据字段
                    self.cards[card_uuid] = InsightCardModel(**card_dict)
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
    
    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> list[InsightCardModel]:
        """
        按日期范围获取卡片记录
        注意：InsightCardModel当前没有日期字段，此方法为预留接口
        """
        # 如果未来InsightCardModel添加了日期字段，可以在此实现日期过滤
        return list(self.cards.values())
    
    def save_all(self, cards_data: list[InsightCardModel]):
        """
        保存当天生成的卡片数据
        
        Args:
            cards_data: 卡片数据字典列表，每个字典包含卡片信息
        """
        for card_model in cards_data:
            # 添加卡片到仓库
            self.add_card(card_model)
            
        print(f"成功保存 {len(cards_data)} 张卡片")