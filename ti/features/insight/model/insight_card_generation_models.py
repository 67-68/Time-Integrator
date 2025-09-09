from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Callable
from PyQt6.QtCore import QObject


@dataclass
class RawCardData:
    """Raw data from detector before presenter processing"""
    id: str
    data: Dict[str, Any]
    weight: Optional[float] = None


@dataclass
class PresentedCardData:
    """Data after presenter processing, ready for display"""
    card_type: str
    judgement_key: List[str]
    sementic_key: str
    data: Dict[str, Any]
    weight: float
    id: str


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
class ActionUnit:
    """Basic action unit data structure"""
    start_time: str
    end_time: str
    category: str
    metadata: Dict[str, Any]


@dataclass
class AnalyzerConfig:
    """Configuration for analyzer functions"""
    matcher: Callable


@dataclass
class FixedCardResult:
    """Result from fixed card analysis with additional metadata"""
    card_type: str
    judgement_key: List[str]
    sementic_key: str
    data: Dict[str, Any]
    weight: float
    id: str
    duration: str
    card_type_id: str


@dataclass
class CacheCardData:
    """Data structure for cache storage"""
    card_id: str
    id: str
    weight: float
    data: Dict[str, Any]


@dataclass
class CacheCategoryData:
    """Data structure for cache category storage"""
    data: List[CacheCardData]
    total: Dict[str, Any]