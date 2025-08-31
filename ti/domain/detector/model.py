"""_summary_
这个文件存储所有登记的配方Enum id
所有配方组装需要的强类型类
"""

from dataclasses import dataclass

from ti.core.Interfaces.detector_Interface import DetectorInterface
from ti.core.analysis.matchers import Matcher
from enum import Enum

from ti.features.intervention.model.model import INVEvent

class BaseDetectorState(Enum):
    HOOK = "hook"
    RESULT = "result"

class Detector_Recipe_ID(Enum):
    POST_EAT_WASTE = "post_eat_waste"

@dataclass
class Detector_State:
    state_name: str #这里就不用Enum了，太固定
    matcher: Matcher

@dataclass
class Detector_Sequence:
    hook: list[Detector_State]
    result: list[Detector_State]

@dataclass
class Detector_Config:
    sequence: Detector_Sequence
    card_type_id = None #卡片id，用于查找资料，在创建的时候被给予

@dataclass
class Detector_Recipe:
    """_summary_
    最上层的数据类
    """
    detector: type[DetectorInterface]
    config: Detector_Config
    