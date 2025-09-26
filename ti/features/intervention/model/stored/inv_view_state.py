from pydantic import BaseModel

from ti.features.intervention.model.events.inv_view_event import INVViewEvent
from ti.features.intervention.model.events.special_events import INVSpecialEvent


class StatePresentation(BaseModel):
    button: dict[str,INVViewEvent]
    title: str

class ViewState(BaseModel):
    """_summary_
    这个类表示一个状态要包含的东西
    对应状态key + 它的所有规则
    """
    name: str
    transition: dict[INVViewEvent,str] # str是viewstate.name
    presentation: StatePresentation
    entering_event: list[INVSpecialEvent] = [] #按理来说会存储INV_Special_Events类的value
    
class INVViewRecipe(BaseModel):
    """
    卡片和presenter的配方
    """
    view_id: str
    state: dict[str,ViewState]
    initial_state: str