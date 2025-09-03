from dataclasses import dataclass
from enum import Enum


class ActionLength(Enum):
    HOUR = "hour"
    MINUTE = "minute"
    HALF_HOUR = "half_hour"

class ActionType(Enum):
    WORK = "work" | "w"
    WASTE = "waste" | "s"
    REST = "rest" | "r"

@dataclass
class Action:
    action_id: str # action类id
    action_display_name: str # 展示什么，一般是中文
    default_task_stream: str | None # 默认的任务流
    default_environment: str | None # 默认上下文
    default_length: ActionLength | int | None
    default_action_type: ActionType | str

    default_importance: bool | None
    default_urgency: bool | None
    # 设定这么多default, 需要如何判定呢？在未来的输入语法中，action会被率先输入吗，还是输入之后更改时间什么的？