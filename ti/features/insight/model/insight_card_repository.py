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
                "card_uuid": card.card_uuid,
                # 新增元数据字段
                "create_time": card.create_time.isoformat() if card.create_time else None,
                "duration": card.duration,
                "current_state": card.current_state,
                "data_uuid": card.data_uuids,
                "detector_recipe_id": card.detector_recipe_id,
                "cache": card.cache
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
                    # 使用from_dict方法来自动处理所有字段，包括新增的元数据字段
                    self.cards[card_uuid] = InsightCardModel.from_dict(card_dict)
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
    
    def save_today_cards(self, cards_data: list[dict]):
        """
        保存当天生成的卡片数据
        
        Args:
            cards_data: 卡片数据字典列表，每个字典包含卡片信息
        """
        from ti.features.insight.model.insight_card_model import InsightCardModel
        
        for card_dict in cards_data:
            # 创建完整的卡片数据字典，包含所有元数据
            full_card_data = {
                'sementic_text': card_dict.get('sementic_key', ''),
                'judgements_texts': card_dict.get('judgement_key', []),
                'title_text': card_dict.get('card_type', ''),
                'color': card_dict.get('color', '#3498DB'),
                'icon_path': card_dict.get('icon_path', ''),
                'icon_color': card_dict.get('icon_color', '#3498DB'),
                'card_type_id': card_dict.get('card_type_id', card_dict.get('id', '')),
                'card_uuid': card_dict.get('id', str(uuid.uuid4())),
                # 元数据字段
                'create_time': datetime.now().isoformat(),
                'duration': 'today',
                'current_state': 'generated',
                'data_uuid': card_dict.get('data_uuid'),
                'detector_recipe_id': card_dict.get('detector_recipe_id')
            }
            
            # 使用from_dict方法创建卡片模型
            card_model = InsightCardModel.from_dict(full_card_data)
            
            # 添加卡片到仓库
            self.add_card(card_model)
        
        print(f"成功保存 {len(cards_data)} 张当天卡片")