from dataclasses import dataclass
from typing import List, Dict, Any
from ti.core.Interfaces.basic_event import BasicEvent


class InsightEvent(BasicEvent):
    pass

@dataclass
class SaveInsightCard(InsightEvent):
    event_id: str = "save_insight_card"
    card_uuid: str = None

@dataclass
class InsightCardGenerationStarted(InsightEvent):
    """洞察卡片生成开始事件"""
    event_id: str = "insight_card_generation_started"
    report_type: str = "yesterday"  # yesterday, today, custom

@dataclass
class RecipeLoaded(InsightEvent):
    """配方加载完成事件"""
    event_id: str = "recipe_loaded"
    fixed_recipes_count: int = 0
    conditional_recipes_count: int = 0

@dataclass
class CardGenerated(InsightEvent):
    """单个卡片生成完成事件"""
    event_id: str = "card_generated"
    card_id: str = None
    card_type: str = None  # fixed, conditional, stored
    card_data: Dict[str, Any] = None

@dataclass
class AllCardsGenerated(InsightEvent):
    """所有卡片生成完成事件"""
    event_id: str = "all_cards_generated"
    total_cards: int = 0
    fixed_cards: int = 0
    conditional_cards: int = 0
    stored_cards: int = 0

@dataclass
class CardRendered(InsightEvent):
    """卡片渲染到界面事件"""
    event_id: str = "card_rendered"
    card_id: str = None
    ui_component: Any = None

@dataclass
class InsightGenerationCompleted(InsightEvent):
    """洞察生成流程完成事件"""
    event_id: str = "insight_generation_completed"
    success: bool = True
    error_message: str = None