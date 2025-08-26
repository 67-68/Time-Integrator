from dataclasses import dataclass
from enum import Enum

from ti.domain.detector.baseDetector import BaseDetector
from ti.features.intervention.view.card import InterventionCard

class Intervention_ID(Enum):
    POST_EAT_WASTE = "post_eat_waste"
    

class InterventionEvent(Enum):
    """_summary_
    同样表示当前的状态
    在统计数据“大体上是否同意的时候”可以用得到
    """
    USER_ACCEPTED = "choice_accept"
    USER_REJECTED = "choice_giveUp" #使用narrative中的文本

@dataclass
class InterventionState:
    """_summary_
    这个类表示一个状态要包含的东西
    对应状态key + 它的所有规则
    """
    name: str
    transitions: dict[InterventionEvent,str]
    
@dataclass
class InterventionRecipe:
    intervention_id: str
    state: dict[str,InterventionState]
    initial_state: str
    detector: type[BaseDetector]
    
@dataclass
class InterventionFactory_Pack:
    ui: InterventionCard
    recipe: InterventionRecipe
    