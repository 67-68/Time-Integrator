from dataclasses import dataclass
import datetime
from typing import Any


@dataclass
class SelectionCondition:
    """
    这个类作为ContextSelection返回的数据模型
    规定了应该怎么样查找数据基类
    通过每个数据模型都应该有的属性查找
    """
    data_type: Any # 应该是DataModel类本身
    
    date: datetime.date = None
    