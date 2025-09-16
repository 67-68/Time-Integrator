
from dataclasses import dataclass


@dataclass    
class SynthesizerRegistry:
    """
    用来规范需要传递的数据
    """
    syn_id: str
    func: callable # 会把数据塞进去