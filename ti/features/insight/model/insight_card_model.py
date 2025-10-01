from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional

from pydantic import BaseModel

from ti.model.duration import Duration
from ti.features.detector.service.matchers import Matcher

class InsightCardModel(BaseModel):
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
    data_uuids: dict[str,str] = {}  # 关联的数据UUID, key为每个数据的状态，来源于配方
    detector_recipe_id: Optional[str] = None  # 检测器配方ID



