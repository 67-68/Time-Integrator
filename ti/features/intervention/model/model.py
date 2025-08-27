from dataclasses import dataclass
from enum import Enum

from ti.domain.detector.baseDetector import BaseDetector

class INV_ID(Enum):
    POST_EAT_WASTE = "post_eat_waste"    

class INVEvent(Enum):
    """_summary_
    同样表示当前的状态
    在统计数据“大体上是否同意的时候”可以用得到
    """
    USER_ACCEPTED = "choice_accept"
    USER_REJECTED = "choice_giveUp" #使用narrative中的文本
    INTERVENTION_CREATED = "intervention_created"

@dataclass
class INV_State_Btn:
    return_event: INVEvent
    text: str

@dataclass
class INV_State_Presentation:
    button: dict[INV_State_Btn]
    title: str

@dataclass
class INVState:
    """_summary_
    这个类表示一个状态要包含的东西
    对应状态key + 它的所有规则
    """
    name: str
    transition: dict[INVEvent,str]
    presentation: INV_State_Presentation
    
@dataclass
class INVRecipe:
    intervention_id: str
    state: dict[str,INVState]
    initial_state: str
    detector: type[BaseDetector]


    
