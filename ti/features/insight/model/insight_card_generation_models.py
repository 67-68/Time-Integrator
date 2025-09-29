from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Callable
from PyQt6.QtCore import QObject

from ti.features.insight.model.insight_card_model import InsightCardModel


@dataclass
class RawCardData:
    """Raw data from detector before presenter processing"""
    id: str
    data: Dict[str, Any]
    weight: Optional[float] = None

@dataclass
class CardInfo:
    """Information about a card including detector and presenter"""
    detector: QObject
    id: str
    presenter: Callable

@dataclass
class Recipe:
    """Base recipe structure"""
    id: str
    duration: str


@dataclass
class FixedRecipe(Recipe):
    """Recipe for fixed cards with analyzer"""
    analyzer: Callable
    analyzer_config: Dict[str, Any]
    presenter: Callable


@dataclass
class ConditionalRecipe(Recipe):
    """Recipe for conditional cards with detector"""
    detector: str
    presenter: Callable

@dataclass
class AnalyzerConfig:
    """Configuration for analyzer functions"""
    matcher: Callable

@dataclass
class CacheCardData:
    """Data structure for cache storage"""
    card_id: str
    id: str
    weight: float
    data: Dict[str, Any]
