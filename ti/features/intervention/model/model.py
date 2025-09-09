from dataclasses import dataclass,asdict,field
from datetime import datetime
from enum import Enum
from uuid import uuid4
import uuid

from ti.core.Interfaces.detector_Interface import DetectorInterface
from ti.model.duration import Duration

class INV_View_ID(Enum):
    POST_EAT_WASTE = "post_eat_waste"  
    UNSETTLING_HEART = "unsettling_heart"
    POST_BASH_WASTE = "post_bash_waste"  

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
    special_event: list[str] = None #按理来说会存储INV_Special_Events类的value
    
@dataclass
class INV_View_Recipe:
    """
    卡片和presenter的配方
    """
    view_id: str
    state: dict[str,INVState]
    initial_state: str
    detector: type[DetectorInterface]

@dataclass
class INV_Contract:
    create_time: datetime = field(default_factory=datetime.now)
    duration: str = None
    solve_time: datetime = None
    solved: bool = None #用户是否看到了干涉，或者说干涉无论是否被接受，它被激发了没有
    success: bool = None # 用户最后是否接受了干涉
    contract_uuid: str = field(default_factory=lambda: str(uuid4()))
    contract_category_id: str = None
    current_state: str = None
    view_recipe_id: str = None
    detector_recipe_id: str = None #这是一个非常不好的设计...我知道
    
    def to_dict(self) -> dict:
        """将实例序列化为字典。"""
        data = asdict(self)
        data["create_time"] = self.create_time.isoformat()
        if self.solve_time:
            data["solve_time"] = self.solve_time.isoformat()
        return data
        
    @classmethod
    def from_dict(cls, data: dict) -> 'INV_Contract':
        """从字典反序列化为实例。"""
        # 将ISO格式的字符串，转换回datetime对象
        if data.get('create_time'):
            data['create_time'] = datetime.fromisoformat(data['create_time'])
        if data.get('solve_time'):
            data['solve_time'] = datetime.fromisoformat(data['solve_time'])
        return cls(**data)

    # 按理来说这里应该还有一个即使接受了干涉，之后是否成功的字段和它的数据模型
    # 但是我没做 
    # 或许可以看作干涉契约转化为展示之后的再一次干涉/数据收集 
    # 这个可以和干涉本身解耦吗？

class INV_Contract_State(Enum):
    BEFORE_START = "before_start"
    AGREED = "agreed" #user同意了但还没有录入monitor
    ACTIVE = "active"
    COMPLETE = "complete"
    GHOST = "ghost" # 用来当作占位符，直到timeSpan结束之后消散允许新的contraction出现

@dataclass
class INV_Contract_Recipe:
    contract_recipe_id: str #也是contract category id
    duration: Duration
    view_recipe_id: str
    
@dataclass
class INV_Entity_Recipe:
    insight_card_category_id: str
    entity_recipe_id: str
    contract_recipe: str
    view_recipe_id: str #这种东西永远使用id而不是原本的配方
    

class INV_Special_States(Enum):
    ACCEPTED_CONTRACT = "accepted_contract"
    END_INTERVENTION = "end_intervention"

@dataclass
class INV_Contract_Context:
    """
    表示一个actionUnit的数据
    """
    action: str
    date: datetime|str
    start: str
    end: str
    action_detail: str

@dataclass
class INV_ContractLog:
    """
    这个类用来存储contract被归档之后的数据
    """
    # === 无默认值的字段放前面 ===
    original_contract_id: str
    log_category_id: str
    original_contract_category_id: str
    user_id: str
    created_at: datetime
    resolved_at: datetime
    final_willingness_status: str
    
    # === 有默认值的字段放后面 ===
    log_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    willingness_decision_at: datetime | None = None
    execution_triggered_at: datetime | None = None
    final_execution_status: str | None = None
    willingness_notes: str | None = None
    execution_notes: str | None = None
    trigger_context: dict = None
    
    def to_dict(self) -> dict:
        """将日志实例序列化为字典"""
        data = asdict(self)
        data["created_at"] = self.created_at.isoformat()
        data["resolved_at"] = self.resolved_at.isoformat()
        if self.willingness_decision_at:
            data["willingness_decision_at"] = self.willingness_decision_at.isoformat()
        if self.execution_triggered_at:
            data["execution_triggered_at"] = self.execution_triggered_at.isoformat()
        return data
        
    @classmethod
    def from_dict(cls, data: dict) -> 'INV_ContractLog':
        """从字典反序列化为日志实例"""
        if data.get('created_at'):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        if data.get('resolved_at'):
            data['resolved_at'] = datetime.fromisoformat(data['resolved_at'])
        if data.get('willingness_decision_at'):
            data['willingness_decision_at'] = datetime.fromisoformat(data['willingness_decision_at'])
        if data.get('execution_triggered_at'):
            data['execution_triggered_at'] = datetime.fromisoformat(data['execution_triggered_at'])
        return cls(**data)


    

from typing import Dict, Any

@dataclass
class INV_View_Model:
    """
    这个类用来存储Model的数据
    同样使用于json数据库
    """
    # === 身份标识 ===
    view_id: str #配方可以通过它查找
    view_uuid: str
    
    # === 数据存储 ===
    current_state: str
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将模型转换为字典，用于JSON序列化
        """
        return {
            "view_id": self.view_id,
            "view_uuid": self.view_uuid,
            "current_state": self.current_state
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'INV_View_Model':
        """
        从字典创建模型实例，用于JSON反序列化
        """
        return cls(
            view_id=data.get("view_id", ""),
            view_uuid=data.get("view_uuid", ""),
            current_state=data.get("current_state", "")
        )