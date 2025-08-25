from dataclasses import dataclass
from enum import Enum

from ti.features.intervention.view.card import InterventionCard

@dataclass
class InterventionRecipe:
    intervention_id: str
    detector = None
    state:list[str]

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
    这个类表示当前的状态
    包括大概的事件/状态和具体的ID
    同样的结构用来读取
    """
    event: InterventionEvent
    sementic_id: str
    
@dataclass
class InterventionFactory_Pack:
    ui: InterventionCard
    recipe: InterventionRecipe
    