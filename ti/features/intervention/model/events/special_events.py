"""
特殊的事件
使用@dataclass编码
被Reducer获取并处理Model
"""
from dataclasses import dataclass
from typing import ClassVar

from ti.features.intervention.view.interventionCard import InterventionCard


@dataclass
class INVSpecialEvent:
    """特殊事件基类"""
    event_id: str

    def __str__(self) -> str:
        return self.event_id


@dataclass
class InterveneUserEvent(INVSpecialEvent):
    """用户干预事件"""
    event_id: ClassVar[str] = "intervene_user"


@dataclass
class AddToInsightCardEvent(INVSpecialEvent):
    """添加到洞察卡片事件"""
    view: InterventionCard
    insight_card_id: str 
    event_id: ClassVar[str] = "add_to_insight_card"
    
    
    