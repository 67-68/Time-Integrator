from dataclasses import dataclass
from pydantic import BaseModel
from ti.core.Interfaces.basic_event import BasicEvent
from ti.features.intervention.model.events.special_events import INVSpecialEvent

@dataclass
class InterventionTriggered():
    """
    这个事件表示某个干涉项目被Trigger了
    即事件流入
    """
    inv_project_id: str
    event_id: str = "intervention_triggered"
    special_events: list[INVSpecialEvent] = None
    
    