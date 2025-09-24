from dataclasses import asdict, dataclass, field
from datetime import datetime
from uuid import uuid4


from ti.features.refactored_intervention.model.inv_reducer import INVReducer
from ti.features.refactored_intervention.presenter.IIntervention_Presenter import IInterventionPresenter
from ti.features.refactored_intervention.service.IIntervention_Event_Source import IInterventionEventSource



@dataclass(frozen=True)
class InterventionProject:
    """
    这个类作为一个干涉的基础
    """
    EventSource: list[type[IInterventionEventSource]]
    reducer: type[INVReducer]
    view: list[type[IInterventionPresenter]]
    
@dataclass
class INVProjectModel:
    """
    这个类保持一个Project的数据
    """
    # --- 元信息
    create_time: datetime = field(default_factory=datetime.now)
    duration: str = None
    solve_time: datetime = None
    current_state: str = None
    
    # --- 时间信息
    solved: bool = None #用户是否看到了干涉，或者说干涉无论是否被接受，它被激发了没有
    condition_met:bool = None
    success: bool = None # 用户最后是否接受了干涉
    
    # --- 身份标识
    contract_uuid: str = field(default_factory=lambda: str(uuid4()))
    project_id: str
    
    def to_dict(self) -> dict:
        """将实例序列化为字典。"""
        data = asdict(self)
        data["create_time"] = self.create_time.isoformat()
        if self.solve_time:
            data["solve_time"] = self.solve_time.isoformat()
        # data["view_recipe_id"] = data["view_recipe_id"].value
        return data
        
    @classmethod
    def from_dict(cls, data: dict) -> 'INVProjectModel':
        """从字典反序列化为实例。"""
        # 将ISO格式的字符串，转换回datetime对象
        if data.get('create_time'):
            data['create_time'] = datetime.fromisoformat(data['create_time'])
        if data.get('solve_time'):
            data['solve_time'] = datetime.fromisoformat(data['solve_time'])
        return cls(**data)

@dataclass
class INVProjectModelUpdated:
    model: INVProjectModel