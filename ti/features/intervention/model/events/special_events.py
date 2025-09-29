"""
特殊的事件
使用Enum编码
被Reducer获取并处理Model
"""
from enum import Enum


class INVSpecialEvent(Enum):
    INTERVENE_USER = "intervene_user" 
    ADD_TO_INSIGHT_CARD = "add_to_insight_card"
    