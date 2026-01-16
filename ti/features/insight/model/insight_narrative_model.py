from pydantic import BaseModel
from typing import Dict, List, Optional


class InsightNarrativeModel(BaseModel):
    """
    洞察叙事数据模型
    用于存储和管理洞察卡片的叙事文本
    """
    narrative_id: str
    narrative_type: str  # "universal", "specific", "presentation"
    action_type: Optional[str] = None  # 仅用于specific类型
    narrative_key: Optional[str] = None  # "sementic_key", "judgement_key", "presentation"
    text: List[str] = []
    
    def get_random_text(self) -> Optional[str]:
        """随机获取一个叙事文本"""
        if self.text:
            import random
            return random.choice(self.text)
        return None