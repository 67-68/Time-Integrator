
from dataclasses import dataclass
from enum import Enum


class INVViewEvent(Enum):
    """
    这个类用来定义card的event
    也就是说，按钮返回的事件 
    供内部View-Card使用
    相当于，选择分枝使用的东西
    

    Args:
        Enum (_type_): _description_
    """
    USER_ACCEPTED = "user_accepted"
    USER_REJECTED = "user_rejected"

@dataclass
class INVViewStateEvent:
    previous_state: str
    new_state:str
    project_id:str
    view_id: str

    