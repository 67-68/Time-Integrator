from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional

from ti.features.detector.baseDetector import BaseDetector
from ti.model.duration import Duration
from ti.features.detector.matchers import Matcher


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
    
    # 新增元数据字段，参考intervention contracts
    create_time: datetime = field(default_factory=datetime.now)
    duration: str = "today"  # 默认今天
    current_state: str = "generated"  # 状态: generated, viewed, archived
    data_uuids: dict[str] = None  # 关联的数据UUID, key为每个数据的状态，来源于配方
    detector_recipe_id: Optional[str] = None  # 检测器配方ID
    
    # 插件使用，按理来说里面的每一个key是每一个插件的名字，每个value是插件的数据
    # 同时，每个dict的value都需要支持to_dict和from_dict
    cache: dict = None
    
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
            "card_uuid": self.card_uuid,
            # 新增元数据字段
            "create_time": self.create_time.isoformat() if self.create_time else None,
            "duration": self.duration,
            "current_state": self.current_state,
            "data_uuid": self.data_uuids,
            "detector_recipe_id": self.detector_recipe_id,
            # 缓存字段
            "cache": self.cache
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'InsightCardModel':
        """
        从字典创建模型实例，用于JSON反序列化
        """
        # 处理时间字段
        create_time_str = data.get("create_time")
        create_time = datetime.fromisoformat(create_time_str) if create_time_str else datetime.now()
        
        return cls(
            sementic_text=data.get("sementic_text", ""),
            judgements_texts=data.get("judgements_texts", []),
            title_text=data.get("title_text", ""),
            color=data.get("color", "#3498DB"),
            icon_path=data.get("icon_path", ""),
            icon_color=data.get("icon_color", "#3498DB"),
            card_type_id=data.get("card_type_id", ""),
            card_uuid=data.get("card_uuid", ""),
            # 新增元数据字段
            create_time=create_time,
            duration=data.get("duration", "today"),
            current_state=data.get("current_state", "generated"),
            data_uuids=data.get("data_uuid", None),
            detector_recipe_id=data.get("detector_recipe_id", None),
            # 缓存字段
            cache=data.get("cache", None)
        ) 
    
@dataclass
class AnalyzerConfig:
    matcher: Matcher

@dataclass
class AnalyzerRecipe:
    analyzer_type: None # 目前的analyzer使用的都是函数，需要类化
    analyzer_config: AnalyzerConfig

@dataclass
class InsightFixCardRecipeModel:
    card_type_id: str
    analyzer_recipe: AnalyzerRecipe
    
class InsightCondCardRecipeModel:
    detector_type_id: str
    presenter: None # 需要类化
    duration: Duration    


