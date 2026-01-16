# 用来创建一个按钮的数据模型 
# capture page接受这个来创建按钮
from dataclasses import dataclass


@dataclass
class ModeBtn:
    page_id: str # 关联的界面id
    text: str # 按钮显示什么