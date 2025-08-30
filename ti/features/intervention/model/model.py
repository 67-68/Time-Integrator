from dataclasses import dataclass,asdict,field
from datetime import datetime
from enum import Enum
from uuid import uuid4

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
class INV_View_Recipe:
    """
    卡片和presenter的配方
    """
    intervention_id: str
    state: dict[str,INVState]
    initial_state: str
    detector: type[BaseDetector]

@dataclass
class INV_Contract:
    create_time: datetime = field(default_factory=datetime.now)
    duration: str = None
    solve_time: datetime = None
    solved: bool = None
    success: bool = None
    contract_id: str = uuid4()
    contract_category_id: str = None
    current_state: str = None
    recipe_id: str = None
    
    def to_dict(self) -> dict:
        """将实例序列化为字典。"""
        data = asdict(self)
        data["create_time"] = self.create_time.isoformat()
        data["solve_time"] = self.solve_time.isoformat()
        
    def from_dict(cls, data: dict) -> 'INV_Contract':
        """从字典反序列化为实例。"""
        # 将ISO格式的字符串，转换回datetime对象
        data['create_time'] = datetime.fromisoformat(data['create_time'])
        data['solve_time'] = datetime.fromisoformat(data['solve_time'])
        return cls(**data)


class INV_Contract_Duration(Enum):    
    TODAY = "today"

class INV_Contract_State(Enum):
    BEFORE_START = "before_start"
    ACTIVE = "active"
    COMPLETE = "complete"

@dataclass
class INV_Contract_Recipe:
    contract_recipe_id: str #也是contract category id
    duration: INV_Contract_Duration
    
@dataclass
class INV_Entity_Recipe:
    insight_card_category_id: str
    entity_recipe_id: str
    contract_recipe: str
    view_recipe_id: str #这种东西永远使用id而不是原本的配方
    
