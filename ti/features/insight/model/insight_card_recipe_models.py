"""
Insight Card Recipe Pydantic models for YamlRepository
"""

from pydantic import BaseModel
from typing import Dict, List, Any


class FixedRecipe(BaseModel):
    """Fixed insight card recipe"""
    id: str
    analyzer: str
    analyzer_config: Dict[str, Any]
    presenter: str
    duration: str


class ConditionalRecipe(BaseModel):
    """Conditional insight card recipe"""
    detector: str
    presenter: str
    duration: str