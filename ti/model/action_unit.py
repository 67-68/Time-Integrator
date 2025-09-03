from dataclasses import dataclass
import datetime


@dataclass
class ActionUnit:
    start: datetime
    end: datetime
    action: str
    action_type: str
    action_detail: str
    