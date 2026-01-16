"""_summary_
这个文件存储所有登记的配方Enum id
所有配方组装需要的强类型类
"""

from pydantic import BaseModel
from typing import List, Optional

from ti.core.Interfaces.detector_Interface import DetectorInterface
from ti.features.detector.service.matchers import Matcher
from enum import Enum

# from ti.features.intervention.model.model import INVEvent  # Removed unused import

class BaseDetectorState(Enum):
    HOOK = "hook"
    RESULT = "result"

class Detector_Recipe_ID(Enum):
    POST_EAT_WASTE = "post_eat_waste"
    UNSETTLING_HEART = "unsettling_heart"
    POST_BASH_WASTE = "post_bash_waste"

class Detector_State(BaseModel):
    state_name: str
    matcher: str  # 存储matcher字符串，运行时解析

class Detector_Sequence(BaseModel):
    hook: List[Detector_State]
    result: List[Detector_State]

class Detector_Config(BaseModel):
    sequence: Detector_Sequence
    card_type_id: Optional[str] = None

class Detector_Recipe(BaseModel):
    """_summary_
    最上层的数据类
    """
    recipe_id: str
    detector: str  # 存储detector类型字符串
    config: Detector_Config
    