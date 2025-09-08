from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class InsightCardModel:
    """
    这个类用来定义每一张insight_card应该存储什么数据
    被insightCardPresenter使用
    是json持久化数据的蓝本
    """
    
    sementic_text: str
    judgements_texts: list[str]
    title_text: str
    color: str
    icon_path: str
    icon_color: str
    card_type_id: str #也就是sementic_key
    card_uuid: str
    
    def __str__(self):
        return (f"InsightCardModel(card_type_id='{self.card_type_id}', "
                f"title='{self.title_text}', "
                f"sementic_length={len(self.sementic_text)}, "
                f"judgements_count={len(self.judgements_texts)})")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将模型转换为字典，用于JSON序列化
        """
        return {
            "sementic_text": self.sementic_text,
            "judgements_texts": self.judgements_texts,
            "title_text": self.title_text,
            "color": self.color,
            "icon_path": self.icon_path,
            "icon_color": self.icon_color,
            "card_type_id": self.card_type_id,
            "card_uuid": self.card_uuid
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'InsightCardModel':
        """
        从字典创建模型实例，用于JSON反序列化
        """
        return cls(
            sementic_text=data.get("sementic_text", ""),
            judgements_texts=data.get("judgements_texts", []),
            title_text=data.get("title_text", ""),
            color=data.get("color", "#3498DB"),
            icon_path=data.get("icon_path", ""),
            icon_color=data.get("icon_color", "#3498DB"),
            card_type_id=data.get("card_type_id", ""),
            card_uuid=data.get("card_uuid", "")
        ) 
    
    
