from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Callable
from PyQt6.QtCore import QObject


@dataclass
class RawCardData:
    """Raw data from detector before presenter processing"""
    id: str
    data: Dict[str, Any]
    weight: Optional[float] = None


@dataclass
class BaseCardData:
    """Base card data with shared attributes, cache, and serialization"""
    card_type: str
    judgement_key: List[str]
    sementic_key: str
    data: Dict[str, Any]
    weight: float
    id: str
    cache: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert dataclass to dictionary for serialization"""
        return {
            'card_type': self.card_type,
            'judgement_key': self.judgement_key,
            'sementic_key': self.sementic_key,
            'data': self.data,
            'weight': self.weight,
            'id': self.id,
            'cache': self.cache
        }
    
    @classmethod
    def from_dict(cls, data_dict: Dict[str, Any]) -> 'BaseCardData':
        """Create dataclass from dictionary"""
        return cls(
            card_type=data_dict.get('card_type', ''),
            judgement_key=data_dict.get('judgement_key', []),
            sementic_key=data_dict.get('sementic_key', ''),
            data=data_dict.get('data', {}),
            weight=data_dict.get('weight', 0.0),
            id=data_dict.get('id', ''),
            cache=data_dict.get('cache', {})
        )


@dataclass
class PresentedCardData(BaseCardData):
    """Data after presenter processing, ready for display"""


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

class FixedCardResult(BaseCardData):
    """Result from fixed card analysis with additional metadata"""
    duration: str
    card_type_id: str
    
    def __init__(self, **kwargs):
        # Extract BaseCardData parameters
        base_kwargs = {k: kwargs.pop(k) for k in list(kwargs.keys()) 
                      if k in ['card_type', 'judgement_key', 'sementic_key', 'data', 'weight', 'id', 'cache']}
        
        # Initialize base class
        super().__init__(**base_kwargs)
        
        # Set FixedCardResult specific attributes
        self.duration = kwargs.get('duration', '')
        self.card_type_id = kwargs.get('card_type_id', '')
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert dataclass to dictionary for serialization"""
        base_dict = super().to_dict()
        base_dict.update({
            'duration': self.duration,
            'card_type_id': self.card_type_id
        })
        return base_dict
    
    @classmethod
    def from_dict(cls, data_dict: Dict[str, Any]) -> 'FixedCardResult':
        """Create dataclass from dictionary"""
        return cls(**data_dict)


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