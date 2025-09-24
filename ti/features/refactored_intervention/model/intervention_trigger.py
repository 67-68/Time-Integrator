from dataclasses import dataclass

from ti.core.Interfaces.basic_event import BasicEvent
from ti.features.refactored_intervention.model.special_events import INVSpecialEvent

# 不对...我定义了更多的事件？

@dataclass
class InterventionTriggered(BasicEvent):
    """
    这个事件表示某个干涉项目被Trigger了
    即事件流入
    """
    inv_project_id: str 
    special_events: list[INVSpecialEvent]
    
    