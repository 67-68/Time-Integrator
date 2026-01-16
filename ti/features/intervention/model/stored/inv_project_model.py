from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel

@dataclass
class INVProjectModel(BaseModel):
    """
    这个类保持一个Project的数据
    """
    # --- 身份标识
    project_id: str
    project_uuid: str = field(default_factory=lambda: str(uuid4()))
    
    # --- 元信息
    create_time: datetime = field(default_factory=datetime.now)
    duration: str = None
    solve_time: datetime = None
    current_state: str = None
    
    # --- 时间信息
    solved: bool = None # 用户是否看到了干涉，或者说干涉无论是否被接受，它被激发了没有
    condition_met:bool = None 
    success: bool = None # 用户最后是否接受了干涉

@dataclass
class INVProjectModelUpdated:
    model: INVProjectModel