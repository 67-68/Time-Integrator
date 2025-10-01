from pydantic import BaseModel
from typing import Dict, Any, List, Optional


class InsightCacheData(BaseModel):
    """Data model for insight cache storage"""
    id: str
    data: List[Dict[str, Any]]
    total: Dict[str, Any]


class InsightCacheEntry(BaseModel):
    """Individual cache entry"""
    card_id: str
    id: str
    weight: float
    data: Dict[str, Any]