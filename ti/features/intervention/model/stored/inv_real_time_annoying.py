"""
用来隔一分钟响铃annoying people功能的配方和运行中存储的数据模型
"""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class RealTimeAnnoying:
    action_name: str
    action_detail: str # 会在干扰的时候展示
    start_time: datetime