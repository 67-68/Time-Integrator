from dataclasses import dataclass, field
from datetime import date

from ti.core.Interfaces.basic_event import BasicEvent
from ti.model.action_unit import ActionUnit

@dataclass(frozen=True)
class CaptureState:
    """
    代表capture 插件的唯一真理
    所有的插件状态被存储在这里
    """
    current_date: date = field(default_factory=date.today())
    current_date_action_units: dict[str,ActionUnit] = field(default_factory=dict)
    selected_unit_id: str | None = None
    smart_input_text: str
    
    def get_current_unit(self) -> ActionUnit | None:
        return self.current_date_action_units.get(self.selected_unit_id,None)