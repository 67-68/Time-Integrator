# features/narratives/models.py
from pydantic import BaseModel, Field
from typing import List, Dict

# 自底向上地定义模型

class PresentationTexts(BaseModel):
    """定义一个具体表现形式（如card_success）下的文本。"""
    title: List[str]

class SemanticKeys(BaseModel):
    """定义语义文本。"""
    text: List[str]
    history_text: List[str] = Field(default_factory=list)

class JudgementKeys(BaseModel):
    """定义评价文本。"""
    # 使用 Dict[str, List[str]] 来允许任意的judgement_key
    # e.g., "praise": [...], "doubt_accuracy": [...]
    judgements: Dict[str, List[str]] = Field(default_factory=dict)

class NarrativeRecipe(BaseModel):
    """
    这是一个完整的、强类型的“叙事配方”模型。
    它完美地映射了你YAML文件的结构。
    """
    presentation: Dict[str, PresentationTexts]
    semantic_key: SemanticKeys