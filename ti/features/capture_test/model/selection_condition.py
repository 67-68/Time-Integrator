from dataclasses import dataclass
import datetime


@dataclass
class SelectionCondition:
    """
    这个类作为ContextSelection返回的数据模型
    规定了应该怎么样查找数据基类
    通过每个数据模型都应该有的属性查找
    """
    data_type: str
    
    date: datetime.date = None
    